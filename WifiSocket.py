#!WifiSocket.py

import Events
import Report
import socket
import sys

def EventHandler(eventId, eventArg):
    global s
    if Events.ids.POSTINIT == eventId:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''  #socket.gethostname()
        port = 54321
        s.bind((host, port))
        s.listen()
        print("Listening on port", port)
        s.setblocking(0) # Non-blocking socket
    if Events.ids.SEC == eventId:
        try:
            client, addr = s.accept()
        except:
            return # Ignore any error, since that just means the client hasn't contacted us this time
        else:
            dictText = Report.MakeText() # Keep time up to date
            print("WiFi sending:", dictText)
            client.send(bytes(dictText, "utf-8"))
            client.close()
