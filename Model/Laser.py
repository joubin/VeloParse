from Parser.Parse import get_int_value


class Laser(object):
    def __init__(self, distance, intensity):
        self.distance = distance
        self.intensity = intensity

    def __str__(self, *args, **kwargs):
        return self.__str_intensity()

    def __str_basic(self):
        return "Distance: " + str(self.distance)\
                + " Intensity: " + str(self.intensity)

    def __str_intensity(self):
        return self.intensity

    def __repr__(self, *args, **kwargs):
        return str(self.intensity)

    @classmethod
    def create_from_hex_data(cls, distance, intensity):
        distance = get_int_value(distance)
        intensity = get_int_value(intensity)
        return cls(distance, intensity)
