# !Events.py

from enum import Enum, auto
import ESP32_Server
import WifiSocket
import BluetoothSocket
import Weather
import Report

class ids(Enum):
    INIT = auto()
    POSTINIT = auto()
    SEC = auto()

def Issue(eventId, eventArg=0):
    #ESP32_Server.EventHandler(eventId, eventArg)
    WifiSocket.EventHandler(eventId, eventArg)
    BluetoothSocket.EventHandler(eventId, eventArg)
    Weather.EventHandler(eventId, eventArg)
    #Report.EventHandler(eventId, eventArg)
