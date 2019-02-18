from manage_firbebase import ManageFirebase


class Data:

    _temp: float
    _humidity: int
    _rain: bool
    _cloud: bool
    _smoke: bool
    _fire: bool
    _fan: bool
    _led: bool

    def __init__(self):
        self._firebase = ManageFirebase()
        self.temp = 0.0
        self.humidity = 0
        self.rain = False
        self.cloud = False
        self.smoke = False
        self.fire = False
        self.fan = False
        self.led = False

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        self._firebase.add_sensor_data({u'temp': value})
        self._temp = value

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        self._firebase.add_sensor_data({u'humidity': value})
        self._humidity = value

    @property
    def rain(self):
        return self._rain

    @rain.setter
    def rain(self, value):
        self._firebase.add_sensor_data({u'rain': value})
        self._rain = value

    @property
    def cloud(self):
        return self._cloud

    @cloud.setter
    def cloud(self, value):
        self._firebase.add_sensor_data({u'cloud': value})
        self._cloud = value
