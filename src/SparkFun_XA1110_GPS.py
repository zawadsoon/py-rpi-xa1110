import smbus
import math
import time

class SparkFun_XA1110_GPS:
    'Driver for SparkFun GPS Breakout - XA1110 (Qwiic) that uses I2C'
    MAX_PACKET_SIZE = 255
    CHUNK_SIZE = 32
    CHUNKS_COUNT = 8

    def __init__ (self, address = 0x10, bus_number = 1):
        self.address = address
        self.bus_number = bus_number
        self.data = [] 
        self.smbus = smbus.SMBus(bus_number)
        print("Conecting to 0x" + str(format(self.address, '02x')) + " on bus " + str(self.bus_number))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.smbus.close()
        print("Closing to 0x" + str(format(self.address, '02x')) + " on bus " + str(self.bus_number))

    def receiveData (self, maxPacketSize = None, chunkSize = None):
        """Receive data from GPS device"""
        if maxPacketSize is None:
            maxPacketSize = SparkFun_XA1110_GPS.MAX_PACKET_SIZE
        if chunkSize is None:
            chunkSize = SparkFun_XA1110_GPS.CHUNK_SIZE

        self.data = []
        counter = 0
        while (counter < maxPacketSize):
            readedI2CBlockData = self.smbus.read_i2c_block_data(
                self.address, 
                chunkSize 
            )
            for n in range(0, chunkSize):
                if readedI2CBlockData[n] is not 0x0A: 
                    self.data.append(readedI2CBlockData[n])
                    counter += 1

    def available (self):
        return bool(self.data)

    def ascii (self):
        """Returns received bytes decoded as ASCII"""
        return bytearray(self.data).decode('ascii').split('\r')

    def bytes (self):
        return self.data

    def sendData (self, packet):
        if len(packet) > 255:
            raise Exception("Command message to long")

        #we send 32 bytes in chunk but in last one we send ony 31
        #it is because we want to send 256 bytes, byt we count from 0
        # and we have from 0 to 255, if last chunk will have 32 bytes
        # then we will have 257 bytes that we try to send
        for n in range(0, SparkFun_XA1110_GPS.CHUNKS_COUNT):
            i = n*SparkFun_XA1110_GPS.CHUNK_SIZE
            nums = list(
                map(
                    lambda x: ord(x), 
                    packet[i:i+SparkFun_XA1110_GPS.CHUNK_SIZE-1]
                )
            )
            self.smbus.write_i2c_block_data(
                self.address,
                SparkFun_XA1110_GPS.CHUNK_SIZE,
                nums
            )
            time.sleep(0.02)

    def createMTKPacket (self, packetType, data):
        """
        Creates $PMTK packet

        Keyword arguments:
        packetType - number that indicates packet type
        data - extra data that will be send in packet
        """
        #default header
        configSequence = "$PMTK"

        #Attach leading zeros
        if packetType < 100: 
            configSequence += "0"
        if packetType < 10: 
            configSequence += "0"
        
        configSequence += str(packetType)

        if data:
            configSequence += data

        configSequence += "*" + self.getCRC(configSequence) + '\r' + '\n'
        return configSequence
    
    def getCRC (self, sequence):
        bytes = bytearray([0]) + bytearray(sequence[1: -1], 'ascii')

        for n in range(len(bytes)):
            bytes[0] ^= bytes[n]

        crcAsStr = format(bytes[0], '02x')
        return "0"+crcAsStr if bytes[0] < 10 else crcAsStr
