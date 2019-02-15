import serial
import json

serialport = serial.Serial("/dev/ttyACM0", 9600)

temp = {'action': 4}
jsonObj = json.dumps(temp)
serialport.write(jsonObj.encode('utf-8'))

while True:
    command = serialport.readline()
    commandDecoded = json.loads(command)
    print(commandDecoded)
