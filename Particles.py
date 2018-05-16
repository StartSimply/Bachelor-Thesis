import pickle
from Vector import Vector
import os
# import glob


class Particles(object):

    def __init__(self, dimension=int()):
        self.pole = []
        self.number = 0
        self.dimension = dimension

    def dictionary(self):
        particles_dict = {'pole': [particle.dictionary() for particle in self.pole],
                          'number': self.number,
                          'dimension': self.dimension
                          }
        return particles_dict

    def save(self, project_id=str(), simulation_number=None):
        if not os.path.exists('Dataset/Particles/'+project_id):
            os.makedirs('Dataset/Particles/' + project_id)
            # files = glob.glob("/home/adam/*.txt")
        pickle.dump(self.dictionary(), open('Dataset/Particles/' + project_id + '/' + str(simulation_number), 'wb'))

    @staticmethod
    def load(project_id = str(), sub_id=str(), simulation_number=None, implementation=False):
        if implementation:
            saved_particles = pickle.load(open(project_id + sub_id + 'Particles/' + str(simulation_number), 'rb'),
                                          encoding='latin1')
        else:
            saved_particles = pickle.load(open('Dataset/Particles/' + project_id +'/'+str(simulation_number), 'rb'), encoding='latin1')

        loaded_particles = Particles()
        for saved_particle in saved_particles['pole']:
            loaded_particles.pole.append(Particle.load(saved_particle=saved_particle))
            loaded_particles.number += 1
        loaded_particles.dimension = saved_particles['dimension']
        return loaded_particles

    def add(self, number=int(), position=None):
        for i in range(number):
            self.pole.append(Particle.create(position=position, dimension=self.dimension))
            self.number += 1

    def new_position(self, wind=None, gravity=None, walls=None):
        for particle in self.pole:
            particle.make_step(dimension=self.dimension, wind=wind, gravity=gravity, walls=walls)


class Particle(object):

    def __init__(self, set_position=None, dimension=None):
        if not set_position:
            self.position = Vector()
        elif set_position:
            self.position = Vector.list_input(position_list=set_position, dimension=dimension)

    def dictionary(self):
        particle_dict = {'position': self.position.dictionary()}
        return particle_dict

    @staticmethod
    def load(saved_particle=None):
        loaded_particle = Particle()
        loaded_particle.position = Vector.load(saved_vector=saved_particle['position'])
        return loaded_particle

    def make_step(self, dimension=None, wind=None, gravity=None, walls=None):
        self.position.random_step(dimension=dimension, wind=wind, gravity=gravity, walls=walls)

    @staticmethod
    def create(dimension=None, position=None):
        new_particle = Particle(set_position=position, dimension=dimension)
        return new_particle


if __name__ == '__main__':
    project_id = str(0)

    particles = Particles(dimension=2)
    particles.add(number=3, position=[0,0,0])
    particles.save(project_id=project_id, simulation_number=0)

    particles.new_position()
    particles.save(project_id=project_id, simulation_number=1)

    particles = Particles.load(project_id=project_id, simulation_number=1)
    print(particles.dictionary())
