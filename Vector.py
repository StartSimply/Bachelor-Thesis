import random
import numpy
from math import sqrt, atan


class Vector(object):

    def __init__(self,  x_axis=0, y_axis=0, z_axis=0):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis

    def __repr__(self):
        repr_text = str(self.dictionary())
        return repr_text

    def random_step(self, dimension=int(), wind=None, gravity=None, walls=None):
        if wind:
            dilatation_vector = wind.vector
            dilatation_vector = self.sum(vector1=self.generate_vector(dimension=dimension), vector2=dilatation_vector)
            self.update(self.sum(vector1=self, vector2=dilatation_vector))

        else:
            dilatation_vector = self.generate_vector(dimension=dimension)
            self.update(to_vector=self.sum(vector1=self, vector2=dilatation_vector))

        if walls:
            for wall in walls.pole:
                if wall.x_axis:
                    if wall.x_orientation*self.x_axis >= wall.x_axis*wall.x_orientation:
                        self.x_axis = 2*wall.x_axis - self.x_axis
                if wall.y_axis:
                    if wall.y_orientation*self.y_axis >= wall.y_axis*wall.y_orientation:
                        self.y_axis = 2*wall.y_axis - self.y_axis

    def update(self, to_vector):
        self.x_axis = to_vector.x_axis
        self.y_axis = to_vector.y_axis
        self.z_axis = to_vector.z_axis

    def normalize(self):
        r_size = self.get_amplitude()
        self.x_axis /= r_size
        self.y_axis /= r_size
        self.z_axis /= r_size

    def set_amplitude(self, amplitude):
        self.normalize()
        self.x_axis *= amplitude
        self.y_axis *= amplitude
        self.z_axis *= amplitude

    def get_amplitude(self):
        amplitude = sqrt(self.x_axis**2 + self.y_axis**2 + self.z_axis**2)
        return amplitude

    def get_list(self):
        vector_list = [self.x_axis, self.y_axis, self.z_axis]
        return vector_list

    def get_distance(self, other_vector=None):
        vector_sum = self.sum(vector1=self, vector2=self.invert(vector_to_invert=other_vector))
        distance = vector_sum.get_amplitude()
        return distance

    def clone(self):
        cloned_vector = Vector()
        cloned_vector.x_axis = self.x_axis
        cloned_vector.y_axis = self.y_axis
        cloned_vector.z_axis = self.z_axis
        return cloned_vector

    @staticmethod
    def invert(vector_to_invert):
        vector_to_invert.x_axis *= -1
        vector_to_invert.y_axis *= -1
        vector_to_invert.z_axis *= -1
        return vector_to_invert

    @staticmethod
    def generate_vector(dimension=int()):
        new_vector = Vector()
        if dimension == 1:
            new_vector.x_axis = float(random.choice([-1,1]))
        elif dimension >= 2:
            phi = random.uniform(0, 2*numpy.pi)
            if dimension == 3:
                theta = random.uniform(0, numpy.pi)
                new_vector.x_axis = numpy.cos(phi / numpy.pi * 180) * numpy.sin(theta / numpy.pi * 180)
                new_vector.y_axis = numpy.sin(phi / numpy.pi * 180) * numpy.sin(theta / numpy.pi * 180)
                new_vector.z_axis = numpy.cos(theta / numpy.pi * 180)
            else:
                new_vector.x_axis = numpy.cos(phi / numpy.pi * 180)
                new_vector.y_axis = numpy.sin(phi / numpy.pi * 180)
        return new_vector

    @staticmethod
    def sum(vector1=None, vector2=None):
        vector_sum = Vector()
        vector_sum.x_axis = vector1.x_axis + vector2.x_axis
        vector_sum.y_axis = vector1.y_axis + vector2.y_axis
        vector_sum.z_axis = vector1.z_axis + vector2.z_axis
        return vector_sum

    @staticmethod
    def create():
        new_vector = Vector()
        return new_vector

    @staticmethod
    def list_input(position_list, dimension=int()):
        new_vector = Vector()
        new_vector.x_axis = position_list[0]
        new_vector.y_axis = position_list[1]
        new_vector.z_axis = position_list[2]
        return new_vector

    @staticmethod
    def load(saved_vector=None):
        loaded_vector = Vector()
        loaded_vector.x_axis = saved_vector['x_axis']
        loaded_vector.y_axis = saved_vector['y_axis']
        loaded_vector.z_axis = saved_vector['z_axis']

        return loaded_vector

    def dictionary(self):
        vector_dict = {'x_axis': self.x_axis, 'y_axis': self.y_axis, 'z_axis': self.z_axis}
        return vector_dict


class RadialVector(object):

    def __init__(self, radius=float(), phi=float(), theta=float()):
        self.radius = radius
        self.phi = phi
        self.theta = theta

    def update(self, to_vector):
        self.radius = to_vector.radius
        self.phi = to_vector.phi
        self.theta = to_vector.theta

    def cartesian_to_radial(self, cartesian_vector=None):
        self.radius = cartesian_vector.get_amplitude()
        self.phi = atan(cartesian_vector.y_axis / cartesian_vector.x_axis)
        self.theta = atan(cartesian_vector.z_axis / sqrt((cartesian_vector.y_axis**2) + (cartesian_vector.x_axis**2)))


if __name__ == '__main__':

    pass
