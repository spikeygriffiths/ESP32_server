#!Report.py

import Events
import Weather
import time
from datetime import datetime

def GetTimeInWords():
    numbers = ['Twelve', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve']
    hours = datetime.now().hour % 12
    minutes = datetime.now().minute
    if minutes >= 33: hours = hours + 1 # For "Quarter to ..."
    if hours > 12: hours = 1
    hourTxt = numbers[hours]
    #return "This line should be two lines"
    if (minutes >= 58) or (minutes < 3):
        return hourTxt + " o\'clock"
    elif minutes < 8:
        return "Five past " + hourTxt
    elif minutes < 13:
        return "Ten past " + hourTxt
    elif minutes < 18:
        return "Quarter past " + hourTxt
    elif minutes < 23:
        return "Twenty past " + hourTxt
    elif minutes < 28:
        return "Twenty Five past " + hourTxt
    elif minutes < 33:
        return "Half past " + hourTxt
    elif minutes < 38:
        return "Twenty Five to " + hourTxt
    elif minutes < 43:
        return "Twenty to " + hourTxt
    elif minutes < 48:
        return "Quarter to " + hourTxt
    elif minutes < 53:
        return "Ten to " + hourTxt
    elif minutes < 58:
        return "Five to " + hourTxt
    return "Can't get here!"

def MakeText():
    #global forecastPeriod
    #global cloudText, symSym, severestSymbol, severestGroup, severestSub
    #global maxTemp, minTemp
    #global maxWind, windText, windDir
    weatherDict = dict()
    weatherDict["period"] = Weather.forecastPeriod
    weatherDict["icon"] = str(Weather.symSym)[4:]
    weatherDict["cloudText"] = Weather.cloudText
    weatherDict["maxTemp"] = str(round(Weather.maxTemp))+"C"
    weatherDict["minTemp"] = str(round(Weather.minTemp))+"C"
    weatherDict["windSpeed"] = str(round(Weather.maxWind))
    weatherDict["windDir"] = str(Weather.windDir)
    weatherDict["windText"] = Weather.windText
    now = datetime.now()
    weatherDict["timeDigits"] = str(now.strftime("%H:%M"))
    weatherDict["timeText"] = GetTimeInWords()
    weatherDict["dayOfWeekText"] = str(now.strftime("%A"))
    weatherDict["dayOfMonthText"] = str(int(now.strftime("%d")))# Use int() to remove leading zero
    weatherDict["monthText"] = str(now.strftime("%B"))
    return str(weatherDict)  # Ready for sending via socket to client
