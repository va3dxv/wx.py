#!/usr/bin/python
#
# wx.py
#
# 19/12/2018
#
# Brian Graves - VA3DXV
#
# va3dxv@gmail.com
#
# This script requires tts_audio.sh and API access to voicerss.org
# calls tts_audio.sh to create .ul file for asterisk
#
# Also requires 'requests' and 'xmltodict' module for python:
# sudo apt-get install python-pip
# sudo python -m pip install xmltodict
# sudo python -m pip install requests
#
# Run this file from root crontab to create the audio file every 4 hours
# 0 */1 * * * /usr/local/sbin/wx.py -c >/dev/null 2>&1
# 5 */2 * * * /usr/local/sbin/wx.py -f >/dev/null 2>&1
#
# add to /etc/asterisk/rpt.conf under [functions]
# 86=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/wxcurrent"
# 87=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/wxforecast"
#####################################
import argparse
import requests
import xmltodict
import subprocess
import shlex
#
# configuration
#
localxmlfeed="http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000070_e.xml"
#
# LISTING of XML feeds and their cities, here:
# http://dd.weather.gc.ca/citypage_weather/xml/siteList.xml
# Corresponds to ACTUAL XML feeds here:
# http://dd.weather.gc.ca/citypage_weather/xml/ON (replace ON with your province)
#
# set your voicerss API key here
voicersskey = "yourvoicerssapikeygoeshere"
# set your desired voice language here
voicersslang = "en-us"
# set speed of speech here
voicerssspeed = "-1"
# set format of initial audio before converting to ulaw
voicerssformat = "44khz_16bit_mono"
#
#
# end configuration
#
temppath = "/tmp/"
aslpath = "/etc/asterisk/custom/"
scriptname = "wx"
aslfile = aslpath + "wx"
ffiletxt = temppath + scriptname + "forecast.txt"
ffilemp3 = temppath + scriptname + "forecast.mp3"
ffilewav = temppath + scriptname + "forecast.wav"
ffileul = aslfile + "forecast.ul"
cfiletxt = temppath + scriptname + "current.txt"
cfilemp3 = temppath + scriptname + "current.mp3"
cfilewav = temppath + scriptname + "current.wav"
cfileul = aslfile + "current.ul"

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="Grab forecast and convert to speech.", action = "store_true", default=False)
parser.add_argument("-c", help="Grab current conditions and convert to speech.", action = "store_true", default=True)

args = parser.parse_args()

xml_data = requests.get(
    url=localxmlfeed
)
weather_data = xmltodict.parse(xml_data.text)
# forecast weather
if args.f:
    print ("tts forecast wx")
    file = open(ffiletxt, "w")
    file.write("Forecast for Eastern Ontario...\r\n")
    for forecast in weather_data["siteData"]["forecastGroup"]["forecast"][0:4]:
            file.write("%s, %s. \r\n" % (
            forecast["period"]["#text"],
            forecast["textSummary"]
    ))
    file.write("End of forecast.\r\n")
    file.close()

    bandreport = open(ffiletxt, "r")
    getmp3 = requests.get("http://api.voicerss.org/",
                          data={"key": voicersskey, "r": voicerssspeed,
                                "src": bandreport, "hl": voicersslang, "f": voicerssformat}
                          )
    bandreport.close()
    mp3file = open(ffilemp3, "wb")
    mp3file.write(getmp3.content)
    mp3file.close()
# convert to wav with lame (apt-get install lame) then to ulaw with sox (apt-get install sox)
    subprocess.call(shlex.split("lame --decode " + ffilemp3 + " " + ffilewav))
    subprocess.call(shlex.split("sox -V " + ffilewav + " -r 8000 -c 1 -t ul " + ffileul))
# cleanup
    subprocess.call(shlex.split("rm -f " + ffiletxt))
    subprocess.call(shlex.split("rm -f " + ffilemp3))
    subprocess.call(shlex.split("rm -f " + ffilewav))
# current weather
elif args.c:
    print ("tts current wx")
    file = open(cfiletxt, "w")
    file.write("The temperature is currently %s with a windchill of %s and %s%s humidity. Current windspeed %s%s. Barometric pressure %s %s and %s..\r\n" % \
               (
                   weather_data["siteData"]["currentConditions"]["temperature"]["#text"],
                   weather_data["siteData"]["currentConditions"]["windChill"]["#text"],
                   weather_data["siteData"]["currentConditions"]["relativeHumidity"]["#text"],
                   weather_data["siteData"]["currentConditions"]["relativeHumidity"]["@units"],
                   weather_data["siteData"]["currentConditions"]["wind"]["speed"]["#text"],
                   weather_data["siteData"]["currentConditions"]["wind"]["speed"]["@units"],
                   weather_data["siteData"]["currentConditions"]["pressure"]["#text"],
                   weather_data["siteData"]["currentConditions"]["pressure"]["@units"],
                   weather_data["siteData"]["currentConditions"]["pressure"]["@tendency"],
               )
               )

    file.close()
    bandreport = open(cfiletxt, "r")
    getmp3 = requests.get("http://api.voicerss.org/",
                          data={"key": voicersskey, "r": voicerssspeed,
                                "src": bandreport, "hl": voicersslang, "f": voicerssformat}
                          )
    bandreport.close()
    mp3file = open(cfilemp3, "wb")
    mp3file.write(getmp3.content)
    mp3file.close()
# convert to wav with lame (apt-get install lame) then to ulaw with sox (apt-get install sox)
    subprocess.call(shlex.split("lame --decode " + cfilemp3 + " " + cfilewav))
    subprocess.call(shlex.split("sox -V " + cfilewav + " -r 8000 -c 1 -t ul " + cfileul))
# cleanup
    subprocess.call(shlex.split("rm -f " + cfiletxt))
    subprocess.call(shlex.split("rm -f " + cfilemp3))
    subprocess.call(shlex.split("rm -f " + cfilewav))
