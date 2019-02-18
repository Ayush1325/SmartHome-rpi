import json
from actions import Actions
from weather_data import WeatherData


class Sender:
    def __init__(self, serial_port, db):
        self.serial_port = serial_port
        self.db = db
        self.current_data = WeatherData()

    def start_loop(self):
        while True:
            self.send_data({u'action': Actions.SENSOR_INFO.value})
            self.read_data()

    def send_data(self, data):
        self.serial_port.write(self.msg_to_send(data))

    def msg_to_send(self, msg):
        return json.dumps(msg).encode('utf-8')

    def read_data(self):
        command = self.serial_port.readline()
        msg = self.msg_received(command)
        self.process_data(msg)

    def add_sensor_data(self, data):
        doc_ref = self.db.collection(u'home').document(u'weather')
        doc_ref.update(data)

    def msg_received(self, msg):
        return json.loads(msg)

    def process_data(self, received_data):
        if received_data['action'] == Actions.SENSOR_INFO.value:
            if self.current_data.temp != received_data['temp']:
                temp = {u'temp': received_data['temp']}
                self.add_sensor_data(temp)
                self.current_data.temp = received_data['temp']
            if self.current_data.humidity != received_data['hmd']:
                temp = {u'humidity': received_data['hmd']}
                self.add_sensor_data(temp)
                self.current_data.humidity = received_data['hmd']
            if self.current_data.rain != received_data['rain']:
                temp = {u'rain': received_data['rain']}
                self.add_sensor_data(temp)
                self.current_data.rain = received_data['rain']
            if self.current_data.cloud != received_data['cloud']:
                temp = {u'cloud': received_data['cloud']}
                self.add_sensor_data(temp)
                self.current_data.cloud = received_data['cloud']
