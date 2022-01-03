#------------------------------------------------------------------------------#
# imports                                                                      #
#------------------------------------------------------------------------------#
import machine
from machine import I2C, Pin, RTC
import network
import time
import utime
import socket
import esp32
import time
import ntptime
import picoweb
import BME280
import ssd1306

#------------------------------------------------------------------------------#
# global defines                                                               #
#------------------------------------------------------------------------------#
pin = machine.Pin(2, machine.Pin.OUT)

temp = esp32.raw_temperature()
temp = (((temp - 32) *5)/9)
hum = 99
firstExe = 0
latest_data = {"date": "2022-01-01", "time": "00:00:00", "temperature": "99.9", "humidity": "99.99", "atmospheric_pressure": "999.99", "altitude": "999.99"}

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

bus = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, bus)
rtc = RTC()
Rtctime = rtc.datetime()
#------------------------------------------------------------------------------#
# subfunctions                                                                 #
#------------------------------------------------------------------------------#
def readDieTemp():
    global temp
    temp = esp32.raw_temperature()
    temp = (((temp - 32) *5)/9)

def readBme280Temp():
    global bus, latest_data, RtcTime
    bme280 = BME280.BME280(i2c=bus)

    latest_data["temperature"] = bme280.temperature
    latest_data["atmospheric_pressure"] = bme280.pressure
    latest_data["humidity"] = bme280.humidity
    latest_data["altitude"] = bme280.altitude


    RtcTime = rtc.datetime()
    FormTime = "%04d-%02d-%02d %02d:%02d:%02d" %(RtcTime[0], RtcTime[1], RtcTime[2], RtcTime[4], RtcTime[5], RtcTime[6])
    print("%s - Bme280 Temp: %2.2f °C; Pres: %2.2f hPa; Alt: %2.2f m ASL; Hum : %2.2f %%" %(FormTime, latest_data["temperature"], latest_data["atmospheric_pressure"], latest_data["altitude"], latest_data["humidity"]))
    display.fill(0)
    display.show()
    #time.sleep_ms(100)
    display.text("Date:%04d-%02d-%02d" %(RtcTime[0], RtcTime[1], RtcTime[2]), 1, 1, 1)
    display.text("Time:%02d:%02d:%02d" %(RtcTime[4], RtcTime[5], RtcTime[6]), 1, 11, 1)
    display.text("Temp:%2.1f grad C" %latest_data["temperature"], 1, 21, 1)
    display.text("Pres:%2.1f hPa" %latest_data["atmospheric_pressure"], 1, 31, 1)
    display.text("Alt :%2.1f m ASL" %latest_data["altitude"], 1, 41, 1)
    display.text("Hum :%2.1f %%" %latest_data["humidity"], 1, 51, 1)
    display.show()

    hour = RtcTime[4]
    minute = RtcTime[5]
    second = RtcTime[6]
    day = RtcTime[2]
    month = RtcTime[1]
    year = RtcTime[0]
    date = "%04d-%02d-%02d" %(year, month, day)
    t_day = "%02d:%02d:%02d" %(hour, minute, second)
    latest_data["time"] = t_day
    latest_data["date"] = date


def TimeZoneAdaption():
    global RtcTime
    ntptime.settime()
    RtcTime = rtc.datetime()

    # Dayligth Saving Timer or European Normal Time
    weekday = RtcTime[3]
    day = RtcTime[2]
    month = RtcTime[1]
    localhour = RtcTime[4]
    # swtich from Eropean Normal Time to Daylight Saving Time
    # in March
    if(month == 3):
        # check if actual weekday is a Sunday and end days
        # till end of month is less than a week
        if(((weekday + 1) == 7) and (day > (31 - 5))):
           print("daylight saving time\n")
           localhour = localhour + 2
        # check if actual days till end of the week are greater
        # than days till end of the month
        elif((31 - day) < (7 - (weekday+1))):
            print("daylight saving time\n")
            localhour = localhour + 2
        else:
            print("european normal time\n")
            localhour = localhour + 1
    # Daylight Saving Time from April till September
    elif((month > 3) and (month < 10)):
        print("daylight saving time\n")
        localhour = localhour + 2
    # Switch from Daylight Saving Time to European Normal Time
    # in October
    elif(month == 10):
        # check if actual weekday is a Sunday and end days
        # till end of month is less than a week
        if(((weekday + 1) == 7) and (day > (31 - 5))):
            print("european normal time\n")
            localhour = localhour + 1
        # check if actual days till end of the week are greater
        # than days till end of the month
        elif((31 - day) < (7 - (weekday+1))):
            print("european normal time\n")
            localhour = localhour + 1
        else:
            print("daylight saving time\n")
            localhour = localhour + 2
    # European Normal Time from November till February
    elif((month > 10) or (month < 3)):
        print("european normal time\n")
        localhour = localhour + 1

    # A new day begin
    if(localhour > 23 ):
        localhour = localhour - 24

    print("RtcTime %s %s %s %s %s %s %s %s" %(RtcTime[0], RtcTime[1], RtcTime[2], RtcTime[3], RtcTime[4], RtcTime[5], RtcTime[6], RtcTime[7]))
    RtcTime = rtc.datetime((RtcTime[0], RtcTime[1], RtcTime[2], RtcTime[3], localhour, RtcTime[5], RtcTime[6], RtcTime[7]))


def handleInterrupt(timer):
    global pin, RtcTime
    if(pin.value()):
        pin.off()
    else:
        pin.on()
    readDieTemp()
    readBme280Temp()




#------------------------------------------------------------------------------#
# main                                                                         #
#------------------------------------------------------------------------------#
display.text("ESP32", 1, 1, 1)
display.text("Wetterstation", 1, 11, 1)
display.text("coded by", 1, 21, 1)
display.text("Max Adler", 1, 31, 1)
display.show()
wait_exp = 0

sta_if.active(True)
sta_if.ifconfig(("192.168.2.51", "255.255.255.0", "192.168.2.1", "192.168.2.1"))
sta_if.connect('WLAN_SSID', 'WLAN_PASSWD')

while ((sta_if.isconnected() == False) and (wait_exp < 30) and (sta_if.status()!= 202)):
        time.sleep(1)
        wait_exp += 1
        print("waiting for Network :%d s" %wait_exp)

timer = machine.Timer(0)

timer.init(period=60000, mode=machine.Timer.PERIODIC, callback=handleInterrupt)

if(wait_exp >= 30) or (sta_if.status()== 202):
    display.fill(0)
    display.text("No WLAN", 1, 1, 1)
    display.text("connected", 1, 11, 1)
    display.show()
    sta_if.active(False)

elif(sta_if.isconnected()):
    display.fill(0)
    display.text("WLAN", 1, 1, 1)
    display.text("connection", 1, 11, 1)
    display.text("established", 1, 21, 1)
    display.show()
    print('Network connection to MadMax_WLAN established!\n')
    print(sta_if.ifconfig())
    for i in range(0,3):
        pin.on()
        time.sleep_ms(250)
        pin.off()
        time.sleep_ms(250)

    time.sleep_ms(500)
    TimeZoneAdaption()

    readBme280Temp()

    ip_address = sta_if.ifconfig() [0]
    app = picoweb.WebApp(__name__)
    @app.route("/")
    def send_index(req, resp):
        yield from app.sendfile(resp, 'index.html')

    @app.route("/get_latest_data")
    def get_latest_data(req, resp):
        global  latest_data
        yield from picoweb.jsonify(resp, latest_data)

    app.run(debug=1, host=ip_address, port=80)
