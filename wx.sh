#!/usr/bin/python
import json
import requests
import xmltodict

xml_data = requests.get(
    url="http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000070_e.xml"
)

weather_data = xmltodict.parse(xml_data.text)

file=open("./wxforecast.txt","+w")

file.write("The current temperature is %s degrees celsius, with %s%s humidity. Current winds %s%s." % \
    (
    weather_data["siteData"]["currentConditions"]["temperature"]["#text"],
    weather_data["siteData"]["currentConditions"]["relativeHumidity"]["#text"],
    weather_data["siteData"]["currentConditions"]["relativeHumidity"]["@units"],
    weather_data["siteData"]["currentConditions"]["wind"]["speed"]["#text"],
    weather_data["siteData"]["currentConditions"]["wind"]["speed"]["@units"],
    #weather_data["siteData"]["currentConditions"]["wind"]["direction"],
    )
    )

file.write("\r\nHere is your forecast for Eastern Ontario.\r\n")
for forecast in weather_data["siteData"]["forecastGroup"]["forecast"][0:4]:
    file.write("%s, %s. \r\n" % (
        forecast["period"]["#text"],
        forecast["textSummary"]
    ))
file.write("End of forecast.\r\n")
file.close()
