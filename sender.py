import json
from weather_data import WeatherData
from sensor_data import SensorData
from uno_actions import unoActions
from nano_actions import nanoActions


class Sender:
    def __init__(self, uno, nano, db, data):
        self.uno = uno
        self.nano = nano
        self.current_weather_data = WeatherData()
        self.current_sensor_data = SensorData()
        self.current_device_data = data
        self.db = db

    def start_loop(self):
        while True:
            try:
                self.send_data(self.nano, {u'action': nanoActions.SENSOR_INFO.value})
                self.read_data()
            except:
                continue

    def send_data(self, port, data):
        port.write(self.msg_to_send(data))

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def read_data(self):
        command = self.nano.readline()
        msg = self.msg_received(command.decode('utf-8'))
        self.process_data(msg)

    def add_weather_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'weather')
        doc_ref.update(data)
        
    def add_sensor_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'sensors')
        doc_ref.update(data)

    def add_monitor_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'monitor')
        doc_ref.update(data)

    def add_device_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'devices')
        doc_ref.update(data)

    def msg_received(self, msg):
        return json.loads(msg)

    def process_data(self, received_data):
        if received_data['action'] == nanoActions.SENSOR_INFO.value:
            if self.current_weather_data.temp != received_data['temp']:
                temp = {u'temp': received_data['temp']}
                self.send_data(self.uno, {'action': unoActions.LCD.value, 'temp': received_data['temp'], 'hmd': received_data['hmd']})
                self.add_weather_data(temp)
                self.current_weather_data.temp = received_data['temp']
            if self.current_weather_data.humidity != received_data['hmd']:
                temp = {u'humidity': received_data['hmd']}
                self.send_data(self.uno, {'action': unoActions.LCD.value, 'temp': received_data['temp'], 'hmd': received_data['hmd']})
                self.add_weather_data(temp)
                self.current_weather_data.humidity = received_data['hmd']
            if self.current_weather_data.rain != received_data['rain']:
                temp = {u'rain': received_data['rain']}
                self.add_weather_data(temp)
                self.current_weather_data.rain = received_data['rain']
            if self.current_weather_data.cloud != received_data['cloud']:
                temp = {u'cloud': received_data['cloud']}
                self.add_weather_data(temp)
                self.current_weather_data.cloud = received_data['cloud']
        elif received_data['action'] == nanoActions.EARTHQUAKE.value:
            if not self.current_sensor_data.earth_quake:
                self.add_sensor_data({u'earthQuake': True})
                self.send_data(self.uno, {'action': unoActions.BUZZ.value, 'state': True})
                self.current_sensor_data.earth_quake = True
        elif received_data['action'] == nanoActions.FIRE.value:
            if not self.current_sensor_data.fire:
                self.add_sensor_data({u'fire': True})
                self.send_data(self.uno, {'action': unoActions.BUZZ.value, 'state': True})
                self.current_sensor_data.fire = True
        elif received_data['action'] == nanoActions.SMOKE.value:
            if not self.current_sensor_data.smoke:
                self.add_sensor_data({u'smoke': True})
                self.send_data(self.uno, {'action': unoActions.BUZZ.value, 'state': True})
                self.current_sensor_data.smoke = True
        elif received_data['action'] == nanoActions.FLOOD.value:
            if not self.current_sensor_data.flood:
                self.add_sensor_data({u'flood': True})
                self.send_data(self.uno, {'action': unoActions.BUZZ.value, 'state': True})
                self.current_sensor_data.flood = True
        elif received_data['action'] == nanoActions.RESET.value:
            self.add_sensor_data({u'earthQuake': False, u'fire': False, u'smoke': False, u'flood': False})
            self.send_data(self.uno, {'action': unoActions.BUZZ.value, 'state': False})
            self.current_sensor_data.reset()
        elif received_data['action'] == nanoActions.LED1.value:
            if self.current_device_data.led1 > 0:
                self.send_data(self.uno, {u'action': unoActions.LED1.value, u'value': 0})
                self.current_device_data.led1 = 0
                self.add_device_data({u'light1': 0})
            else:
                self.send_data(self.uno, {u'action': unoActions.LED1.value, u'value': 255})
                self.current_device_data.led1 = 255
                self.add_device_data({u'light1': 255})
        elif received_data['action'] == nanoActions.LED2.value:
            if self.current_device_data.led2 > 0:
                self.send_data(self.uno, {u'action': unoActions.LED2.value, u'value': 0})
                self.current_device_data.led2 = 0
                self.add_device_data({u'light2': 0})
            else:
                self.send_data(self.uno, {u'action': unoActions.LED2.value, u'value': 255})
                self.current_device_data.led2 = 255
                self.add_device_data({u'light2': 255})
        elif received_data['action'] == nanoActions.FAN.value:
            if self.current_device_data.fan > 0:
                self.send_data(self.uno, {u'action': unoActions.FAN.value, u'value': 0})
                self.current_device_data.fan = 0
                self.add_device_data({u'fan': 0})
            else:
                self.send_data(self.uno, {u'action': unoActions.FAN.value, u'value': 255})
                self.current_device_data.fan = 255
                self.add_device_data({u'fan': 255})
        elif received_data['action'] == nanoActions.FLAME.value:
            self.add_monitor_data({u'flame': received_data['state']})
