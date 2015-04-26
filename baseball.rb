require 'mandrill'  
require 'nokogiri'
require 'rest-client'

email_client = Mandrill::API.new ENV['MANDRILL_KEY']
available = 'http://games.espn.go.com/flb/freeagency?leagueId=17672&teamId=3&seasonId=2015#&seasonId=2015&=undefined&context=freeagency&view=stats&version=currSeason'

def generate(link)
  html = RestClient.get(link)
  doc = Nokogiri::HTML(html)
end

def scrape(link, threshold)
  message_body, pickup_order = '<ul>', []
  doc = generate(link)

  player_stats = doc.css('tr.pncPlayerRow').text
                                           .gsub('+', '+ plus')
                                           .split(/[\+|-]/)                                   
  player_stats.each_with_index { |player, i|
    if i < player_stats.length - 1
      player = player.split(',')
      ahead = player_stats[i + 1].split(',')[0]
      if ahead && ahead.include?('plus') && player[0] != nil
        pick_up = ahead.gsub(/[^\d|.]/ , '')  
        pickup_order << {'p' => player[0].gsub(/[^a-z|' ']/i, '')
                                         .gsub('plus', ''), 
                         'i' => pick_up.to_i }
      end
    end
  }
  pickup_order = pickup_order.select {|x| x['i'] > threshold}
                             .sort_by {|x| x['i']}
                             .reverse
  pickup_order.each {|pick|
    message_body += '<li>' + pick['p']  + ' picked up at ' + pick['i'].to_s + '</li>'
  }

  return message_body += '</ul>'
end

 def summary(available)
  {  
   :subject=> "#{Time.now} Pitcher / Catcher Update",  
   :html => available,
   :to=>[  
     {  
       :email=> "ben.brostoff@gmail.com"  
     }  
   ],  
   :from_email=>"ben.brostoff@gmail.com"  
  }  
end

email_client.messages.send(summary(scrape(available, 5)))