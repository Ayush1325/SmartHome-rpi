import json
from weather_data import WeatherData
from sensor_data import SensorData
from uno_actions import unoActions
from nano_actions import nanoActions


class Sender:
    def __init__(self, uno, nano, db):
        self.uno = uno
        self.nano = nano
        self.current_weather_data = WeatherData()
        self.current_sensor_data = SensorData()
        self.db = db

    def start_loop(self):
        while True:
            self.send_data(self.nano, {u'action': nanoActions.SENSOR_INFO.value})
            self.read_data()

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
        elif received_data['action'] == nanoActions.FLAME.value:
            self.add_monitor_data({u'flame': received_data['state']})
