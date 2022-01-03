#!/usr/bin/env python

#------------------------------------------------------------------------------#
# imports                                                                      #
#------------------------------------------------------------------------------#
from pymongo import MongoClient
import pprint
import urllib.request
import json
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

#------------------------------------------------------------------------------#
# global Variables and constants                                               #
#------------------------------------------------------------------------------#
MONGODBPORT = 49153
MONGODBHOST = "192.168.2.37"
ASCENDING = 1
DESCENDING = -1
HISTLIMIT = 60

WEATHERSTATIONHOMEOFFICEADR = "http://192.168.2.51/get_latest_data"

timestamp = "12.08.19"
timestampOld = ""

#------------------------------------------------------------------------------#
# Sub functions                                                                #
#------------------------------------------------------------------------------#

def getDataFromESP():
    global timestamp, timestampOld
    with urllib.request.urlopen(WEATHERSTATIONHOMEOFFICEADR) as url:

        data = json.loads(url.read().decode())
        timestampOld = timestamp
        timestamp = data['time']
        if timestampOld != timestamp:
            print(data)
            client = MongoClient(host=MONGODBHOST, port=MONGODBPORT)
            db = client.weatherstation
            dbData = db.weatherData
            dbData.insert_one(data)
            client.close()

#tutorial1 = {"temperature": 22.98, "altitude": 105.2682, "timeline": "10:07:19", "atmospheric_pressure": 1000.66, "humidity": 46.83594}

#tutorial = db.tutorial
#tutorial.insert_one(tutorial1)

#for doc in tutorial.find().sort('timeline',DESCENDING).limit(HISTLIMIT):
#for doc in tutorial.find():
#    pprint.pprint(doc)
    
#client.close()

#------------------------------------------------------------------------------#
# main                                                                         #
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(getDataFromESP, 'interval', minutes=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
