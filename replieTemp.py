#-*- coding:utf-8 -*- 
from datetime import datetime
import FaBoTemperature_ADT7410
import time
import tweepy
import re
import requests
import json
#import Humidity_HTS221
import FaBoHumidity_HTS221

import twitkey
import cupnudle
import openWM

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

#pattern list

p_temp = r"ラボの温度"
p_wtommorow = r"明日の天気"
p_wtoday = r"今の天気"
p_wntomm = r"明後日の天気"
p_nudle = r"ごつもりガチャ"
w_puni = r"ぷにぴ"
#URL for send tweet

url = "https://api.twitter.com/1.1/statuses/update.json"

#return reply text

def reply_text():
    temp = adt7410.read()
    humi = hts221.readHumi()
    
    tl1 = "コアラのデスクは.\n気温 : %4.2f℃" % temp
    tl2 = "\n湿度 : %4.2f" %  humi + r"%"
    tl3 = "\n体感気温 : %4.2f℃ "%  getExTemp(temp, humi) + "です"
    tl4 = "\n" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    template = tl1 + tl2 + tl3 + tl4
    text =  template
    return text

#get weather information
def weather_text(i):
    wurl = "http://weather.livedoor.com/forecast/webservice/json/v1?city=070030"
    req = requests.get(wurl)

    origin = req.json()
    title = origin["title"].encode("UTF-8")
    data = origin["forecasts"][i] 
    
    max_temp = data["temperature"]["max"]["celsius"].encode('UTF-8')
    date = data["date"].encode('UTF-8')
    telop = data["telop"].encode('UTF-8')  
    print "set some jsons data"
    min_temp = data["temperature"]["min"]["celsius"].encode('UTF-8')

    template =  date + "\n" + title + "\n明日の天気は"+ telop + "。\n最高気温は "+ max_temp + "℃\n" + "最低気温は" + min_temp + "℃の予想です。\n" 
    
    
    text = template + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    

    return text

# cup nudle 
def nudle_text():
    nudle = cupnudle
    template = nudle.get_nudle() +"\n" +  datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return template
 
def punirep():
    template = "ぷにぴ、じゃあないんだよ" + "\n" + datetime.now().strftime("%Y%m%d %H:%M:%S")


# real time weather information
def WM_text():
    API_KEY = openWM.API
    URL = "http://api.openweathermap.org/data/2.5/weather" 

    r = requests.get(URL + "?q=Aizu-Wakamatsu-shi,jp&APPID=" + API_KEY)

    data = r.json()

    city = data['name'].encode('UTF-8')
    weather = data['weather'][0]['description'].encode('UTF-8')
    humidity = str(data['main']['humidity'])
    temp = str(data['main']['temp'] - 273.15)
    max_temp = str(data['main']['temp_max'] -273.15)
    min_temp = str(data['main']['temp_min'] - 273.15)
    pressure = str(data['main']['pressure'])
    wind = str(data['wind']['speed'])


    template = "Get city:" +  city + "\n"+ weather + "\nTemp :" + temp + "℃\nHumidity :" + humidity + "%℃\nWind:"+ wind +"m/s\nPressure :" + pressure + "hPa\n" +datetime.now().strftime("%H:%M:%S")
   
    return template

#tweet upload method
def update_text(status, template):
    reply = status.id
    scr_name = status.author.screen_name.encode("UTF-8")
    text = "@" + scr_name +"\n"+ template
    api.update_status(text,reply)

    return True


class myException(Exception): pass


#stream Listener. If you change bot behavior, you add code on_status 
class Listener(tweepy.StreamListener):
    def on_status(self, status):
        
        #get tweet and Allocation
        origin_text = status.text.encode("UTF-8")


        if(re.match(p_temp, origin_text)): 
            template = reply_text()
            update_text(status, template)
            
        elif(re.match(p_wtommorow, origin_text)):
            print "launch tommorow"
            template = weather_text(1)
            print "get template"
            update_text(status, template)

        elif(p_nudle in origin_text):
            print "try get nudle"
            template = nudle_text()
            print "get nudle"
            update_text(status, template)

        elif(re.match(p_wtoday, origin_text)):
            print "load today weather"
            template = WM_text()
            print "get template"
            update_text(status, template) 
        elif(re.match(w_puni, origin_text)):
            sname = status.author.screen_name.encode("UTF-8")
            if(sname =="innocent_mame"):
                template = punirep()
                print "puni-pi"
                api.update_status(template)
        return True 
          
    def on_error(self, status_code):
        print "on_error raised"
        print status_code
        raise myException

    def on_timeout(self):
        print('Timeout...')
        raise myException



if __name__ =='__main__':
    listener = Listener()
    stream = tweepy.Stream(auth, listener)
    stream.timeout = None
    
    while True:
        try:
            print "start"
            stream.userstream()
        
        except KeyboardInterrupt:
            exit()
        except:
            print "system reboot"
            stream = tweepy.Stream(auth, listener)
            stream.timeout = None
