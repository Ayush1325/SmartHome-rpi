class WeatherData:

    temp: float
    humidity: int
    rain: bool
    cloud: bool

    def __init__(self):
        self.temp = 0.0
        self.humidity = 0
        self.rain = False
        self.cloud = False
