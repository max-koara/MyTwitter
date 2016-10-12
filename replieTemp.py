#-*- coding:utf-8 -*- 
from datetime import datetime
from requests_oauthlib import OAuth1Session
import FaBoTemperature_ADT7410
import time
import tweepy
import re
import requests
import json
#import Humidity_HTS221
import FaBoHumidity_HTS221

import twitkey
#add method get Experimence temperature
def getExTemp(d_temp, d_humi):

#wind speed = 0m/s in Laboratory, if you have wind speed data, pleese add + 1.4*(wind speed)**0.75

    m_A = 1.76
#Ex_Temp with m_A and Temp and Humi

    Ex_Temp = 37 - ( (37 - d_temp) / (0.68 - 0.0014 * d_humi + 1/m_A) ) - (0.29*d_temp * (1 - (d_humi / 100)))

    return Ex_Temp


#set Temperature and Humidity
adt7410 = FaBoTemperature_ADT7410.ADT7410()
hts221 = FaBoHumidity_HTS221.HTS221()

# tweet blocks

CK = twitkey.twkey['CK']
CS = twitkey.twkey['CS']
AT = twitkey.twkey['AT']
AS = twitkey.twkey['AS']


auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth)


p_temp = r"ラボの温度"
p_weather = r"weather"

#URL for send tweet

url = "https://api.twitter.com/1.1/statuses/update.json"

#return reply text

def reply_text(status):
    temp = adt7410.read()
    humi = hts221.readHumi()
    
    tl1 = "\nコアラのデスクは.\n気温 : %4.2f℃" % temp
    tl2 = "\n湿度 : %4.2f" %  humi + r"%"
    tl3 = "\n体感気温 : %4.2f℃ "%  getExTemp(temp, humi) + "です"
    tl4 = "\n" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    template = tl1 + tl2 + tl3 + tl4
    screen_name = status.author.screen_name.encode("UTF-8")
    text = "@"+ screen_name + template

    return text


def weather_text(status):
    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=070030"
    req = requests.get(url)
    
    data = json.loads(req)
    print data.forecasts
        
    return True
    

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        #if(text == "ping" or text =="  ping" or text == "Ping"):
        origin_text = status.text.encode("UTF-8")
        if(re.match(p_temp, origin_text)): 
            text = reply_text(status)
            reply = status.id
            api.update_status(text,reply)            
         
        elif(re.match(p_weather, origin_temp)):
            weather_text(status)
        
           
        return True 
          
    def on_error(self, status_code):
        print status_code
        return True

    def on_timeout(self):
        print('Timeout...')
        return True



if __name__ =='__main__':

    listener = Listener()
    stream = tweepy.Stream(auth, listener)
    stream.timeout = None
    stream.userstream()

