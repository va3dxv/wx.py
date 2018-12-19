#!/usr/bin/python
# wx.py
# 19/12/2018
#
# Brian Graves - VA3DXV
#
# va3dxv@gmail.com
#
# This script requires tts_audio.sh and API access to voicerss.org
# calls tts_audio.sh to create .ul file for asterisk
#
# Run this file from root crontab to create the audio file every 4 hours
# 0 */1 * * * /usr/local/sbin/wx.py -c >/dev/null 2>&1
# 5 */2 * * * /usr/local/sbin/wx.py -f >/dev/null 2>&1
#
# add to /etc/asterisk/rpt.conf under [functions]
# 86=cmd,asterisk -rx "rpt localplay 47960 /etc/asterisk/custom/wxcurrent"
# 87=cmd,asterisk -rx "rpt localplay 47960 /etc/asterisk/custom/wxforecast"
#####################################################################################################
import argparse
import json
import requests
import xmltodict
import subprocess
import shlex
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="Record forecast and TTS it.", action = "store_true", default=False)
parser.add_argument("-c", help="Record current conditions and TTS it.", action = "store_true", default=True)

args = parser.parse_args()

xml_data = requests.get(
    url="http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000070_e.xml"
)

weather_data = xmltodict.parse(xml_data.text)

if args.f:
    print ("tts forecast wx")
    file = open("/tmp/wxforecast.txt", "w")
    file.write("Forecast for Eastern Ontario...\r\n")
    for forecast in weather_data["siteData"]["forecastGroup"]["forecast"][0:4]:
            file.write("%s, %s. \r\n" % (
            forecast["period"]["#text"],
            forecast["textSummary"]
    ))
    file.write("End of forecast.\r\n")
    file.close()

    subprocess.call(shlex.split("/usr/local/sbin/tts_audio.sh /tmp/wxforecast.txt"))
    subprocess.call(shlex.split("rm -f /tmp/wxforecast.txt"))
    subprocess.call(shlex.split("rm -f /etc/asterisk/custom/wxforecast.ul"))
    subprocess.call(shlex.split("mv /tmp/wxforecast.ul /etc/asterisk/custom"))

elif args.c:
    print ("tts current wx")
    file = open("/tmp/wxcurrent.txt", "w")
    file.write("Current temperature is %s degrees celsius, with %s%s humidity. Current windspeed %s%s.\r\n" % \
               (
                   weather_data["siteData"]["currentConditions"]["temperature"]["#text"],
                   weather_data["siteData"]["currentConditions"]["relativeHumidity"]["#text"],
                   weather_data["siteData"]["currentConditions"]["relativeHumidity"]["@units"],
                   weather_data["siteData"]["currentConditions"]["wind"]["speed"]["#text"],
                   weather_data["siteData"]["currentConditions"]["wind"]["speed"]["@units"],
                   # weather_data["siteData"]["currentConditions"]["wind"]["direction"],
               )
               )
    file.close()

    subprocess.call(shlex.split("/usr/local/sbin/tts_audio.sh /tmp/wxcurrent.txt"))
    subprocess.call(shlex.split("rm -f /tmp/wxcurrent.txt"))
    subprocess.call(shlex.split("rm -f /etc/asterisk/custom/wxcurrent.ul"))
    subprocess.call(shlex.split("mv /tmp/wxcurrent.ul /etc/asterisk/custom"))
