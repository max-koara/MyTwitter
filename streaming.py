#coding: utf-8

import twitkey
import tweepy
from datetime import timedelta

CS = twitkey.twkey['CS']
CK = twitkey.twkey['CK']
AT = twitkey.twkey['AT']
AS = twitkey.twkey['AS']

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
    def on_status(self, status):
     #   status.created_at += timedelta(hours=9)
      #  print status

        #api.update_status("test desu", status.id)
        #print(u"{text}".format(text=status.text))
        #print(u"{name}({screen}) {created} via {src}\n".format(
         #   name=status.author.name, screen = status.author.screen_name,
         #   created=status.created_at, src=status.source))
    
        return True

    def on_event(self, status):
        print status

        return True
    def on_error(self, status_code):
        print('Timeout...')
        return True

    def on_timeout(self):
        print('Timeout...')
        return True




if __name__ == '__main__':
    stream = tweepy.Stream(api.auth, Listener())
    stream.userstream()
            
