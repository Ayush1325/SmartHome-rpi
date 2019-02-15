import serial
from data import Data

serialport = serial.Serial("/dev/ttyACM0", 9600)

dataObj = Data()
temp = {'action': 4}
serialport.write(dataObj.msgToSend(temp))

while True:
    command = serialport.readline()
    print(dataObj.msgRecieved(command))
