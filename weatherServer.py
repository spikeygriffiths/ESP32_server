#!/usr/bin/python3
import socket
import time
from datetime import datetime
from urllib import request, parse
import xml.etree.ElementTree as ET
from enum import Enum, auto

owmApiKey = "590c17ed39950e5bc6648c3f83918987"
owmLocation = "Cambridge,UK"
dayStart = datetime.strptime("08:00:00", "%H:%M:%S")
dayEnd = datetime.strptime("16:00:00", "%H:%M:%S")
eveStart = dayEnd  #datetime.strptime("16:00:00", "%H:%M:%S")
eveEnd = datetime.strptime("23:00:00", "%H:%M:%S")

class Sym(Enum):
    Sun = auto()
    CloudWithSun = auto()
    Moon = auto()
    CloudWithMoon = auto()
    LightCloud = auto()
    DarkCloud = auto()
    LightRain = auto()
    HeavyRain = auto()
    Fog = auto()
    Snow = auto()
    Thunderstorms = auto()
    Unknown = auto()

def owmToSym(symbolVar):
    sym = {
        "01d":Sym.Sun,
        "02d":Sym.CloudWithSun,
        "01n":Sym.Moon,
        "02n":Sym.CloudWithMoon,
        "03d":Sym.LightCloud,
        "03n":Sym.LightCloud,
        "04d":Sym.DarkCloud,
        "04n":Sym.DarkCloud,
        "09d":Sym.LightRain,
        "09n":Sym.LightRain,
        "10d":Sym.HeavyRain,
        "10n":Sym.HeavyRain,
        "50d":Sym.Fog,
        "50n":Sym.Fog,
        "13d":Sym.Snow,
        "13n":Sym.Snow,
        "11d":Sym.Thunderstorms,
        "11n":Sym.Thunderstorms
        }
    return sym.get(symbolVar, Sym.Unknown)

def GetWorstWeather(detail):
    global cloudText, symSym, severestGroup, severestSub
    global maxTemp, minTemp
    global maxWind, windText, windDir
    if detail.tag == "symbol":
        symbolText = detail.attrib["name"] # eg "Broken clouds"
        symbolNumber = int(detail.attrib["number"]) # Group 2xx=Thunderstorm, 3xx=Drizzle, 5xx=Rain, 6xx=Snow, 7xx=Atmosphere, 800=Clear, 8xx=Clouds
        symbolVar = detail.attrib["var"]
        print("("+str(symbolNumber)+")"+symbolText+","+str(symbolVar)+"=="+str(owmToSym(symbolVar)))
        symbolGroup = int(symbolNumber/100)
        symbolSub = symbolNumber % 100
        if symbolGroup==severestGroup:
            if symbolSub>severestSub:
                severestSub=symbolSub
                symSym=owmToSym(symbolVar)
                cloudText=symbolText
        else:
            if symbolGroup==2: # Thunderstorms
                severestGroup=symbolGroup # Nothing beats thunderstorms!
                severestSub=symbolSub
                symSym=owmToSym(symbolVar)
                cloudText=symbolText
            elif symbolGroup==3: # Drizzle
                if severestGroup==8: # Drizzle beats clouds
                    severestGroup=symbolGroup
                    severestSub=symbolSub
                    symSym=owmToSym(symbolVar)
                    cloudText=symbolText
            elif symbolGroup==5: # Rain
                if severestGroup==8 or severestGroup==2: # Rain beats clouds & drizzle
                    severestGroup=symbolGroup
                    severestSub=symbolSub
                    symSym=owmToSym(symbolVar)
                    cloudText=symbolText
            elif symbolGroup==6:
                if severestGroup==8 or severestGroup==2 or severestGroup==5: # Snow beats clouds, drizzle or rain
                    severestGroup=symbolGroup
                    severestSub=symbolSub
                    symSym=owmToSym(symbolVar)
                    cloudText=symbolText
    if detail.tag == "temperature":
        low = float(detail.attrib["min"]) - 273.15 # Convert Kelvin to Celsius
        high = float(detail.attrib["max"]) - 273.15
        print("low temp {0:.1f}".format(low)+" high {0:.1f}".format(high))
        if low < minTemp:
            minTemp = low
        if high > maxTemp:
            maxTemp = high
    if detail.tag == "windSpeed":
        speed = float(detail.attrib["mps"]) * 3.6 # Convert mps to kph
        if speed > maxWind:
            maxWind = speed
            windText = detail.attrib["name"]
    if detail.tag == "windDirection":
        dir = round(float(detail.attrib["deg"]))
        windDir = dir # Might want to try averaging wind direction, rather than just getting last one?

def SetDefaultForecast():
    global cloudText, symSym, severestSymbol, severestGroup, severestSub
    global maxTemp, minTemp
    global maxWind, windText, windDir
    severestSymbol = 800 # 800, Clear sky by default
    severestGroup = int(severestSymbol/100)
    severestSub = severestSymbol % 100
    cloudText = "Clear sky"
    symSym = owmToSym("01d") # Assume clear day sky
    minTemp = 50.0 # Silly low temp
    maxTemp = -20.0 # Silly high temp
    maxWind = 0

def SetUnknownForecast():
    global cloudText, symSym, severestSymbol, severestGroup, severestSub
    global maxTemp, minTemp
    global maxWind, windText, windDir
    severestSymbol = 800 # 800, Clear sky by default
    severestGroup = int(severestSymbol/100)
    severestSub = severestSymbol % 100
    cloudText = "N/A"
    symSym = Sym.Unknown
    minTemp = 50.0 # Silly low temp
    maxTemp = -20.0 # Silly high temp
    maxWind = 0
    windText = "N/A"
    windDir = 0

def GetForecastSlot(forecastSlot):
    for detail in forecastSlot:
        GetWorstWeather(detail) # Need to compare symbolNumber vs previous one to get most extreme weather
    # Now use severestGroup & severestSub to make a Sym

def GetWeatherForecast():
    global forecastPeriod
    global cloudText, symSym, severestSymbol, severestGroup, severestSub
    global maxTemp, minTemp
    global maxWind, windText, windDir
    forecastPeriod = "N/A"
    SetDefaultForecast()
    req = request.Request("https://api.openweathermap.org/data/2.5/forecast?q="+owmLocation+"&mode=xml&appid="+owmApiKey)
    try:
        response = request.urlopen(req)
        root = ET.fromstring(response.read())
        for child in root:
            if child.tag == "forecast":
                for forecastSlot in child:
                    #print(startTime.attrib["from"])
                    start = (datetime.strptime(forecastSlot.attrib["from"],"%Y-%m-%dT%H:%M:%S"))
                    if start.date()==datetime.now().date():
                        print(start.time())
                        if datetime.now().time() < dayEnd.time():
                            if start.time() > dayStart.time() and start.time() < dayEnd.time():
                                forecastPeriod = "Day"
                                GetForecastSlot(forecastSlot)
                        else:
                            if start.time() > eveStart.time() and start.time() < eveEnd.time():
                                forecastPeriod = "Eve"
                                GetForecastSlot(forecastSlot)
    except:
        SetUnknownForecast()
    if forecastPeriod!="N/A":
        severestSymbol = severestGroup * 100 + severestSub

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
    global forecastPeriod
    global cloudText, symSym, severestSymbol, severestGroup, severestSub
    global maxTemp, minTemp
    global maxWind, windText, windDir
    weatherDict = dict()
    weatherDict["period"] = forecastPeriod
    weatherDict["icon"] = str(symSym)[4:]
    weatherDict["cloudText"] = cloudText
    weatherDict["maxTemp"] = str(round(maxTemp))+"C"
    weatherDict["minTemp"] = str(round(minTemp))+"C"
    weatherDict["windSpeed"] = str(round(maxWind))
    weatherDict["windDir"] = str(windDir)
    weatherDict["windText"] = windText
    now = datetime.now()
    weatherDict["timeDigits"] = str(now.strftime("%H:%M"))
    weatherDict["timeText"] = GetTimeInWords()
    weatherDict["dayOfWeekText"] = str(now.strftime("%A"))
    weatherDict["dayOfMonthText"] = str(int(now.strftime("%d")))# Use int() to remove leading zero
    weatherDict["monthText"] = str(now.strftime("%B"))
    return str(weatherDict)  # Ready for sending via socket to client

# Main entry point
global forecastPeriod
global cloudText, symSym
global maxTemp, minTemp
global maxWind, windText
s = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)
host = ''  #socket.gethostname()
port = 54321
updateWeather = time.time() # Update weather immediately after start
s.bind((host, port))
s.listen()
print("Listening with", host,"on port", port)
s.setblocking(0) # Non-blocking socket
while True:
    if time.time() >= updateWeather:
        GetWeatherForecast()
        updateWeather = time.time() + 600 # Only get weather forecast every 10 mins
    try:
        client, addr = s.accept()
    except:
        continue
    else:
        dictText = MakeText() # Keep time up to date
        print("Sending:", dictText)
        client.send(bytes(dictText, "utf-8"))
        client.close()
    time.sleep(1) # 1 sec
