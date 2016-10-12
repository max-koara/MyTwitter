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
p_weather = r"明日の天気"

#URL for send tweet

url = "https://api.twitter.com/1.1/statuses/update.json"

#return reply text

def weather_text():
    wurl = "http://weather.livedoor.com/forecast/webservice/json/v1?city=070030"
    req = requests.get(wurl)
    
    origin = req.json()
    
    data = origin["forecasts"][1]    
    
    max_temp = data["temperature"]["max"]["celsius"].encode('UTF-8')
    min_temp = data["temperature"]["min"]["celsius"].encode('UTF-8')
    date = data["date"].encode('UTF-8')
    telop = data["telop"].encode('UTF-8')      
    print "set some jsons data"
    print type  (max_temp)
    print type (min_temp)
    print type (date)
    print type (telop)
    template = "\n"+ date + "\n明日の天気は"+ telop + "。\n最高気温は "+ max_temp + "℃\n" + "最低気温は" + min_temp + "℃の予想です。\n" 
    text = template
    return text
    

         
text = weather_text()
print "get template weather"
api.update_status(text)



