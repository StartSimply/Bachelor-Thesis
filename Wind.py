from Vector import Vector


class Wind(object):

    def __init__(self):
        self.vector = Vector()
        self.amplitude = 0

    def set(self, x_axis=0, y_axis=0, z_axis=0, amplitude=1):
        self.vector.x_axis = x_axis
        self.vector.y_axis = y_axis
        self.vector.z_axis = z_axis
        self.vector.set_amplitude(amplitude=amplitude)
        self.amplitude = amplitude

    def get_vector(self, dimension):
        wind_vector = Vector()
        if dimension >= 1:
            wind_vector.x_axis = self.vector.x_axis
        if dimension >= 2:
            wind_vector.y_axis = self.vector.y_axis
        if dimension == 3:
            wind_vector.z_axis = self.vector.z_axis
        return wind_vector
