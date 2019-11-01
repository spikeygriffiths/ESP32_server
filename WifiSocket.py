# WifiSocket.py
import socket

def EventHandler(eventId, eventArg):
    if EVENT.POSTINIT == eventId:
        s = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)
        host = ''  #socket.gethostname()
        port = 54321
        s.bind((host, port))
        s.listen()
        print("Listening with", host,"on port", port)
        s.setblocking(0) # Non-blocking socket
    if EVENT.SEC == eventId:
        try:
            client, addr = s.accept()
        except:
            continue
        else:
            dictText = MakeText() # Keep time up to date
            print("WiFi sending:", dictText)
            client.send(bytes(dictText, "utf-8"))
            client.close()
