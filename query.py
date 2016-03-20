import collections, csv

Player = collections.namedtuple('Person', 'name pos val')
_PLAYERS = []

with open('2016.csv', 'rb') as csvfile:
        player_reader = csv.DictReader(csvfile)
        for row in player_reader:
            _PLAYERS.append(Player(
                name=row['Name'],
                pos=row['Position'], 
                val=int(float(row['Weighted']))))

def __format(players):
    for p in players:
        print "{} {} {}".format(p.name, p.pos, p.val)

def query(cond=None, max_val=100, limit=10, ):
    if not cond:
        cond = lambda x: True
    __format(sorted(
        [p for p in _PLAYERS if cond(p) and p.val <= max_val],
        key=lambda p: p.val, reverse=True)[:limit])

def query_by_name(name, max_val=100, limit=10):
    query(lambda x: name in x.name, max_val, limit)

def query_by_pos(pos, max_val=100, limit=10,):
    query(lambda x: pos in x.pos, max_val, limit)
