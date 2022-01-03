# Weatherstation
Smart Home Weatherstation build on a ESP32 board build with Micropython

## Description
The project is split in 3 parts:

 1. uC Soft- and Hardware to: 
    * setup WLAN connection to local network
    * get network time
    * get temperature, humidity and air pressure from mounted sensor
    * calculate altitude in m ASL
    * display timestamp, temperature, humidity, air pressure and altitude on the
    mounted Display
    * setup webserver to: 
        * provide tini web page with same information as on the mounted dispaly
        * provide latest measurement data in JSON format
2. Server for Remote access to the weatherstation with:
    * latest available information and
    * history above the last hour in a nice color graph
3. Experimental setup for MongoDB connection [Draft]

# 1. uC Soft- and Hardware

## Hardware
* [ESP32 NodeMCU Board](https://www.az-delivery.de/collections/mikrocontroller/products/esp32-developmentboard)
* [BMP280 barometric sensor (temperatur, humidity, air pressure)](https://www.az-delivery.de/collections/sensoren/products/gy-bme280)
* [Display SSD1306 (0.96" OLED)](https://www.az-delivery.de/collections/displays/products/0-96zolldisplay)

## uC Software
* [Micropython ESP32 v1.17 (2021-09-02)](https://micropython.org/download/esp32/)


# 2. Server

## Hardware
* Synology NAS DS916+

## Software
* nginx webserver
* python v3.7

# 3. MongoDB
[DRAFT]


# License
Weatherstation is an open-source project and welcomes contribution.
Note that Weatherstation is under the MIT license, and all contributions should follow this license.