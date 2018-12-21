# wx.py
Environment Canada weather text to speech for AllStarLink

19/12/2018

Brian Graves - VA3DXV
va3dxv@gmail.com

Place in /usr/local/sbin

Retreives results from an XML feed:

http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/

This script calls tts_audio.sh to create .ul files for asterisk to play.

tts_audio.sh requires a login and API key from http://voicerss.org

Also requires 'requests' and 'xmltodict' module for python:
sudo apt-get install python-pip && sudo python -m pip install xmltodict && sudo python -m pip install requests

Add to root crontab to create the audio file every X hours

sudo crontab -e:

0 */1 * * * /usr/local/sbin/wx.py -c >/dev/null 2>&1

5 */2 * * * /usr/local/sbin/wx.py -f >/dev/null 2>&1

add to /etc/asterisk/rpt.conf under [functions]

86=cmd,asterisk -rx "rpt localplay 47960 /etc/asterisk/custom/wxcurrent"

87=cmd,asterisk -rx "rpt localplay 47960 /etc/asterisk/custom/wxforecast"
