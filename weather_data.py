class WeatherData:

    _temp: float
    _humidity: int
    _rain: bool
    _cloud: bool
    _smoke: bool
    _fire: bool

    def __init__(self):
        self.temp = 0.0
        self.humidity = 0
        self.rain = False
        self.cloud = False
        self.smoke = False
        self.fire = False
