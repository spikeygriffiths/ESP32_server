# BluetoothSocket.py

# Finds ESP32 devices (or anything that advertises itself as "*ESP32*"

import bluetooth

def BluetoothFindEsp():
    global espBtMac
    devices = bluetooth.discover_devices(lookup_names=True)
    print(type(devices))
    print("BT Devices found:")
    for item in devices:
        print(item)
    # ToDo: Find ESP32's mac and place into espBtMac

def BluetoothInitEsp():
    global BTsocket
    BTsocket = BluetoothSocket(RFCOMM)

def EventHandler(eventId, eventArg):
    global BTsocket, espBtMac
    if EVENT.POSTINIT == eventId:
        # ToDo:  Need a state-driven Bluetooth system to:
        #   find ESP32,
        #   create a socket,
        #   wait for a request from the ESP,
        #   then send the report
    if EVENT.SEC == eventId:
        if espBtMac != NULL:
            BTsocket.connect(espBtMac, 1)
            dictText = MakeText() # Keep time up to date
            print("Bluetooth sending:", dictText)
            BTsocket.send(dictText)
            BTsocket.close()
