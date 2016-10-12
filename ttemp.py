#-*- coding:utf-8 -*- 
from datetime import datetime
from requests_oauthlib import OAuth1Session
import FaBoTemperature_ADT7410
import time

#import Humidity_HTS221
import FaBoHumidity_HTS221

import twitkey
#add method get Experimence temperature
def getExTemp(d_temp, d_humi):

#wind speed = 0m/s in Laboratory, if you have wind speed data, pleese add + 1.4*(wind speed)**0.75

    m_A = 1.76
#Ex_Temp with m_A and Temp and Humi

    Ex_Temp = 37 - ( (37 - d_temp) / (0.68 - 0.0014 * d_humi + 1/m_A) ) - (0.29*d_temp * (1 - (humi / 100)))

    return Ex_Temp


#set Temperature and Humidity
adt7410 = FaBoTemperature_ADT7410.ADT7410()
hts221 = FaBoHumidity_HTS221.HTS221()

# tweet blocks

CK = twitkey.twkey['CK']
CS = twitkey.twkey['CS']
AT = twitkey.twkey['AT']
AS = twitkey.twkey['AS']

#URL for send tweet
url = "https://api.twitter.com/1.1/statuses/update.json"


#tweet

if __name__ == '__main__':
#set Temp:ADT7410 and Humidity:HTS221

    	temp = adt7410.read()
    	humi = hts221.readHumi()

    	#set OAuth session key
    	twitter = OAuth1Session(CK, CS, AT, AS)

        tl1 = "コアラのデスクは.\n気温 : %4.2f℃" % temp
        tl2 = "\n湿度 : %4.2f" %  humi + r"%"
        tl3 = "\n体感気温 : %4.2f℃ "%  getExTemp(temp, humi) + "です"
        tl4 = "\n" + datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
   	template = tl1 + tl2 + tl3 + tl4
	
	#mentenance code 
	#template = "Have a nice day every one. X)"
    	#mentenance code
	params = {"status": template}

	#Oauth and post method
    	req = twitter.post(url, params = params)


	#responce
    	if req.status_code == 200:
        	print("OK")
    	else:
        	print("Error: %d" % req.status_code)
