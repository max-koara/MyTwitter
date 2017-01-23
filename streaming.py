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

class MyException(Exception): pass

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        
        '''
        status has all information of tweet.

        if you get 
        twitter ID of tweet author  > status.authoer.screen_name
        twitter Name                > status.author.name
        tweet text                  > status.text
        favorite count              > status.favorite_count
        tweet id                    > status.id
        tweet ID(if you reply)      > status.in_reply_to_status_id
        and other parameter if you see, please un comment out for the last print 

        function on_status call if stream get new tweet, if you want to add some function for your bot, 
        please add codes in this.

        default this function, if get new tweet, print user-name, user-id and tweet text on your console. 

        if you update tweet, use this function

        api.update_status("hogehuga")

        if you reply ,
        replyid = "tweet_id"
        api.update_status("hogehuga", replyid)
        '''

        print "{username} :@{userid}".format(username=status.author.name.encode("UTF-8"), userid = status.author.screen_name)  
        print status.text
        print        
        
        
        #if you get all parameter of json, please delete comment-out
        #print status
        
        return True

    def on_event(self, status):
        print status

        return True
    def on_error(self, status_code):
        print('Timeout...')
        raise MyException

    def on_timeout(self):
        print('Timeout...')
        raise MyException



if __name__ == '__main__':
    try:    
        stream = tweepy.Stream(api.auth, Listener())
        stream.userstream()
    except KeyboardInterrupt:
        exit()
