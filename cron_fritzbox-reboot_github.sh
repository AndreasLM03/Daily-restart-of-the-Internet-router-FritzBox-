#!/bin/bash

IPS="xxxxxx" # 192.168.178.1
FRITZUSER="xxxxxx" # Username
FRITZPW="xxxxxxx" # Username Password

location="/upnp/control/deviceconfig"
uri="urn:dslforum-org:service:DeviceConfig:1"
action='Reboot'

for IP in ${IPS}; do
	curl -k -m 5 --anyauth -u "$FRITZUSER:$FRITZPW" http://$IP:49000$location -H 'Content-Type: text/xml; charset="utf-8"' -H "SoapAction:$uri#$action" -d "<?xml version='1.0' encoding='utf-8'?><s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'><s:Body><u:$action xmlns:u='$uri'></u:$action></s:Body></s:Envelope>" -s > /dev/null
done