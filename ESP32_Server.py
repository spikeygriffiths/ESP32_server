#!/usr/bin/python3

import time
import Events
import BluetoothSocket # My Bluetooth handler
import WifiSocket # My Wifi handler
import Weather # My weather handler
import Report # My report maker

def main():
    Events.Issue(Events.ids.INIT)
    Events.Issue(Events.ids.POSTINIT)
    while True:
        Events.Issue(Events.ids.SEC, 1)
        time.sleep(1) # 1 sec

if __name__ == "__main__":
    main()