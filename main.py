import serial
from data import Data

serialport = serial.Serial("/dev/ttyACM0", 9600)

dataObj = Data()

while True:
    temp = {'action': 4}
    serialport.write(dataObj.msgToSend(temp))
    command = serialport.readline()
    dataObj.isChanged(dataObj.msgRecieved(command))
