#!/usr/bin/python3
from enum import Enum, auto

import BluetoothSocket # My Bluetooth handler
import WifiSocket # My Wifi handler
import Weather # My weather handler
import Report # My report maker

class EVENT(Enum):
    INIT = auto()
    POSTINIT = auto()
    SEC = auto()

def OSIssueEvent(id, arg):
    OSEventHandler(id, arg)
    WifiSocket.EventHandler(id, arg)
    BluetoothSocket.EventHandler(id, arg)
    Weather.EventHandler(id, arg)
    #Report.EventHandler(id, arg)

# Main entry point
OSIssueEvent(EVENT.INIT, 0)
OSIssueEvent(EVENT.POSTINIT, 0)
while True:
    OSIssueEvent(EVENT.SEC, 1)
    time.sleep(1) # 1 sec
