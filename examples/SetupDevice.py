import os
import sys
import time

sys.path.append('../')

from src.SparkFun_XA1110_GPS import SparkFun_XA1110_GPS

def menuHold ():
    input('\nPress enter to continue')

instr = """Available commands:\n
set1hz:  Set update rate to 1Hz,
set10hz: Set update rate to 1Hz,
setGAA:  Set only NMEA GAA packet,
setAll:  Set all NMEA packets,
version: Get device version,
exit:    Exit/Quit\n"""

def set1hz ():
    with SparkFun_XA1110_GPS() as gps:
        packet = gps.createMTKPacket(220, ",1000")
        gps.sendData(packet) 

def set10hz ():
    with SparkFun_XA1110_GPS() as gps:
        packet = gps.createMTKPacket(220, ",100")
        gps.sendData(packet) 

def setNMEAOnlyGAA ():
    with SparkFun_XA1110_GPS() as gps:
        packet = gps.createMTKPacket(314, ",0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        gps.sendData(packet) 

def setNMEAAll ():
    with SparkFun_XA1110_GPS() as gps:
        packet = gps.createMTKPacket(314, ",-1")
        gps.sendData(packet) 

def getVersion ():
    with SparkFun_XA1110_GPS() as gps:
        #Send command, request version
        packet = gps.createMTKPacket(605, "")
        gps.sendData(packet)

        #Measaure time and check if data was present
        start_time = time.time()
        fetched = False
        elapsed_time = 0

        while fetched is False and elapsed_time < 5:
            gps.receiveData()
            line = gps.ascii()
            if "PMTK" in line:
                print(line)
                fetched = True
            elapsed_time = time.time() - start_time

#Menu
answer=True
while answer:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(instr)
    answer = input("Enter command: ")

    if answer == "set1hz":
        print("\nSetting update rate to 1Hz")
        set1hz()
        menuHold()
    elif answer == "set10hz":
        print("\nSetting update rate to 10Hz")
        set10hz()
        menuHold()
    elif answer == "setGAA":
        print("\nSetting only GAA packet")
        setNMEAOnlyGAA()
        menuHold()
    elif answer == "setAll":
        print("\nSetting all NMEA packets")
        setNMEAAll()
        menuHold()
    elif answer == "version" or answer == 'v':
        print("\nGetting version...")
        getVersion()
        menuHold()
    elif answer == "exit" or answer == 'q':
        print("\nGoodbye") 
        answer = None

