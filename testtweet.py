#-*- coding:utf-8 -*- 
from datetime import datetime
from requests_oauthlib import OAuth1Session
import time
import twitkey
import openWM
import roadWM

CK = twitkey.twkey['CK']
CS = twitkey.twkey['CS']
AT = twitkey.twkey['AT']
AS = twitkey.twkey['AS']

url = "https://api.twitter.com/1.1/statuses/update.json"


#tweet

if __name__ == '__main__':
#set Temp:ADT7410 and Humidity:HTS221

    	#set OAuth session key
    	twitter = OAuth1Session(CK, CS, AT, AS)
	#mentenance code 
	#template = "Have a nice day every one. X)"

        op = roadWM
        city = op.city_name.encode('UTF-8')
        weather = op.weather.encode('UTF-8')
        temp = op.temp.encode('UTF-8')
        max_temp = op.max_temp
        min_temp = op.min_temp
        wind = op.wind
        pressure = op.pressure
     
        template = "Get city:" +  city + "\n"+ weather + "\nTemp :" + temp + "℃\nMax_T:" + max_temp +"℃\nMin_T:"+ min_temp + "℃\nWind:"+ wind +"m/s\nPressure :" + pressure + "hPa\n" +datetime.now().strftime("%H:%M:%S")
    	#mentenance code
	params = {"status": template}

	#Oauth and post method
    	req = twitter.post(url, params = params)


	#responce
    	if req.status_code == 200:
        	print("OK")
    	else:
        	print("Error: %d" % req.status_code)
