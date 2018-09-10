import sys
import time

sys.path.append('../')

from src.SparkFun_XA1110_GPS import SparkFun_XA1110_GPS

#This code gets 255 bytes in each iteration
#Firstly you need to get data from GPS device
#Next this beauty GPS class will keep the data safe in local variable
#Then you get list of NMEA frames decoded into ASCII thanks to ascii() method
#List elements are separated by (carriage return) '\r' sign
#At last we wait some time because GPS device will not send data so fast
#`with` allows to properly close connection automatically
#To break program you can safetly hit Ctrl+C

with SparkFun_XA1110_GPS() as gps:
    lastLine = ""
    for n in range(100):
        gps.receiveData()
        lines = gps.ascii()
        lines[0] = lastLine + lines[0]
        lastLine = lines.pop()
        for line in lines:
            print(line)
        time.sleep(0.9)
