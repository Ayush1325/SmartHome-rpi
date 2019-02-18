import serial
import json
from actions import Actions
from data import Data


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _SerialHelper:
    def __init__(self):
        self.serialport = serial.Serial("/dev/ttyACM0", 9600)
        self.currentData = Data()

    def send_data(self, data):
        self.serialport.write(self.msg_to_send(data))

    def read_data(self):
        command = self.serialport.readline()
        msg = self.msg_recieved(command)
        self.process_data(msg)

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def msg_recieved(self, msg):
        return json.loads(msg)

    def process_data(self, recivedData):
        if recivedData['action'] == Actions.SENSOR_INFO.value:
            if self.currentData.temp != recivedData['temp']:
                self.currentData.temp = recivedData['temp']
            if self.currentData.humidity != recivedData['hmd']:
                self.currentData.humidity = recivedData['hmd']
            if self.currentData.rain != recivedData['rain']:
                self.currentData.rain = recivedData['rain']
            if self.currentData.cloud != recivedData['cloud']:
                self.currentData.cloud = recivedData['cloud']


class SerialHelper(_SerialHelper, metaclass=Singleton):
    pass
