from os import environ
from datetime import datetime
from collections import namedtuple
import unicodedata
import logging
import requests as r
from bs4 import BeautifulSoup as BS
import sendgrid

_log = logging.getLogger(__name__)
_log.addHandler(logging.StreamHandler())
_log.setLevel(logging.DEBUG)

_MY_EMAIL = 'ben.brostoff@gmail.com'
_SGRID_KEY = environ.get('SGRID_KEY')
_EMAIL_CLIENT = sendgrid.SendGridClient(_SGRID_KEY)

Player = namedtuple('Player', 'name owned picked_up')
_batters = {
  'url': 'http://games.espn.go.com/flb/freeagency?leagueId=17672&seasonId=2016',
  'name': 'Batters'
}
_pitchers = {
  'url': _batters['url'] + '&slotCategoryGroup=2',
  'name': 'Pitchers'
}

def _soupify(link):
    return BS(r.get(link).text, 'html.parser')

def _normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ascii','ignore')

def _colorize(val, limit=0):
    if float(val) > limit: return 'green'
    else: return 'black'

def _scrape():
    """
    Fingers crossed ESPN doesn't change their UI...
    """
    html = ''
    for l in _batters, _pitchers:
        html += '<h3>{}</h3>'.format(l['name'])
        players = []
        for row in _soupify(l['url']).select('.playerTableTable tr'):
            try:
                player = row.findAll(class_="playertablePlayerName")
                p_name = _normalize(player[0].text)
                picked_up = _normalize(row.find_all('td')[-1].text)
                owned = _normalize(row.find_all('td')[-2].text)
                if float(picked_up) > 0:
                    players.append(Player(name=p_name, 
                                          owned=owned, picked_up=picked_up ))
            except Exception, e:
                _log.debug('Error getting ESPN update: {}'.format(e))


        for p in sorted(players, key=lambda x: float(x.picked_up), reverse=True): 
              to_add = "<p>{} <span style='color:{}'>{}</span>(<span style='color:{}'>{}</span>)</p>" \
                   .format(p.name, _colorize(p.owned, limit=30), 
                    p.owned, _colorize(p.picked_up, limit=10), p.picked_up)
              html += to_add

    return html

def send():
    message = sendgrid.Mail()
    message.add_to(_MY_EMAIL)
    message.set_from(_MY_EMAIL)
    message.set_subject(datetime.now().strftime("%B %d, %Y") + ' FB2016 Report')
    message.set_html(_scrape())
    sent = _EMAIL_CLIENT.send(message)
    _log.info(sent)

if __name__ == '__main__':
    send()

