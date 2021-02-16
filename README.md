# Daily-restart-of-the-Internet-router-FritzBox-
Everyone is annoyed by the fact that every now and then the Internet stops working properly. The solution is usually a simple reboot of the router. To avoid this, I restart my router every day by a self-written script which is executed on my RaspberryPi minicomputer every day., A good and stable connection in times of HomeOffice is guaranteed



---
## FritzBox Setup

Create a specific username and password on your fritzbox:
<img src= "images/01 fritzbox.jpg" width="800">
<img src= "images/02 fritzbox.jpg" width="800">


---
## Shell Code 


````python
#!/bin/bash

IPS="xxxxxx" # e.g. 192.168.178.1
FRITZUSER="xxxxxx" # Name generated in the Fritzbox interface
FRITZPW="xxxxxxx" # Username Password generated in the Fritzbox interface

location="/upnp/control/deviceconfig"
uri="urn:dslforum-org:service:DeviceConfig:1"
action='Reboot'

for IP in ${IPS}; do
	curl -k -m 5 --anyauth -u "$FRITZUSER:$FRITZPW" http://$IP:49000$location -H 'Content-Type: text/xml; charset="utf-8"' -H "SoapAction:$uri#$action" -d "<?xml version='1.0' encoding='utf-8'?><s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'><s:Body><u:$action xmlns:u='$uri'></u:$action></s:Body></s:Envelope>" -s > /dev/null
done
````


---
## RaspberryPi

Copy cron_fritzbox-reboot_github.sh in this folder : /home/pi/Dokumente/Programme/FritzBox_reboot/

Open terminal and start crontab -e

<img src= "images/03 rasp crontab.jpg" width="800">
<img src= "images/04 rasp crontab.jpg" width="800">

Save crontab by using ctrl + x, type y for y and close the terminal


Your Router will start every day at 540 am
