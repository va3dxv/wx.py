# wx.py
Grabs weather data from environment canada and converts text to u-law audio for Asterisk/app_rpt

01/01/2019

Brian Graves - VA3DXV
va3dxv@gmail.com

Place in /usr/local/sbin

Retreives results from an XML feed:

http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/

This script requires access to http://api.voicerss.org (it's free)

Also requires lame and sox to create the .ul file for asterisk (sudo apt-get install lame && sudo apt-get install sox)

Also requires 'requests' and 'xmltodict' module for python:
sudo apt-get install python-pip && sudo python -m pip install xmltodict && sudo python -m pip install requests

Add to root crontab to create the audio file every X hours

sudo crontab -e:

0 */1 * * * /usr/local/sbin/wx.py -c >/dev/null 2>&1

5 */2 * * * /usr/local/sbin/wx.py -f >/dev/null 2>&1

add to /etc/asterisk/rpt.conf under [functions]
where 86 or 87 are the DTMF control commands you want to use and where 99999 is your node number

86=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/wxcurrent"

87=cmd,asterisk -rx "rpt localplay 99999 /etc/asterisk/custom/wxforecast"
