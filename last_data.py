class lastData:
    __slots__ = ['temp', 'humidity', 'rain', 'cloud']
    temp: float
    humidity: int
    rain: bool
    cloud: bool

    def init(self, _temp, _humidity, _rain, _cloud):
        self.temp = _temp
        self.humidity = _humidity
        self.rain = _rain
        self.cloud = _cloud

    def fromJson(self, data):
        self.temp = data['temp']
        self.humidity = data['hmd']
        self.rain = data['rain']
        self.cloud = data['cloud']
