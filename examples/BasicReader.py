import sys
import time

sys.path.append('../')

from src.SparkFun_XA1110_GPS import SparkFun_XA1110_GPS

#This code gets NMEA frames one by one

with SparkFun_XA1110_GPS(debug = True) as gps:
    for n in range(10):
        gps.receiveData()
        print(gps.ascii())
