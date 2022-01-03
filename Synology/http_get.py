#------------------------------------------------------------------------------#
# imports                                                                      #
#------------------------------------------------------------------------------#
import os
import sys
import time
import json
import urllib.request
import re
#------------------------------------------------------------------------------#
# global defines                                                               #
#------------------------------------------------------------------------------#
temp_hist = {"temperature": [], "atmospheric_pressure": [], "time": [], "date": [], "altitude": [], "humidity": []}
#------------------------------------------------------------------------------#
# Sub functions                                                                #
#------------------------------------------------------------------------------#

def getDataFromESP():
    try:
        with urllib.request.urlopen("http://192.168.2.51/get_latest_data") as url:

            data = json.loads(url.read().decode())
            print(data)
            if temp_hist['time']:
                result = re.match(temp_hist['time'][-1], data['time'])
            else:
                result = False

            if not result:
                temp_hist['temperature'].append(data['temperature'])
                temp_hist['atmospheric_pressure'].append(data['atmospheric_pressure'])
                temp_hist['time'].append(data['time'])
                temp_hist['altitude'].append(data['altitude'])
                temp_hist['humidity'].append(data['humidity'])
                temp_hist['date'].append(data['date'])
                #print(temp_hist)

            if len(temp_hist['temperature']) >= 60:
                del temp_hist['temperature'][0]
                del temp_hist['atmospheric_pressure'][0]
                del temp_hist['time'][0]
                del temp_hist['altitude'][0]
                del temp_hist['humidity'][0]
                del temp_hist['date'][0]

            with open('/volume1/web/temp_hist.json', 'w') as f:
                json.dump(temp_hist, f)
    except:
        print("Host not reachable")
    time.sleep(30)


#------------------------------------------------------------------------------#
# Main Code                                                                    #
#------------------------------------------------------------------------------#
if __name__ == "__main__":
    while(True):
        getDataFromESP()
