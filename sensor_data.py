class SensorData:
    def __init__(self):
        self.earth_quake = False
        self.smoke = False
        self.fire = False
        self.flood = False

    def reset(self):
        self.__init__()
