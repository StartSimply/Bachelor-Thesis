from Particles import Particles
import pickle
import os


class Space(object):
    def __init__(self, project_id):
        self.project_id = project_id

        self.dimension = 0
        self.simulation_number = 0
        self.particles = None
        self.wind = None
        self.gravity = None
        self.lattice = None
        self.walls = None

    def __repr__(self):
        space_repr = str(self.dictionary())
        return space_repr

    def dictionary(self):
        dict_space = {}
        if self.dimension:
            dict_space['dimension'] = self.dimension
        if self.simulation_number:
            dict_space['simulation_number'] = self.simulation_number
        if self.particles:
            dict_space['particles'] = self.particles.dictionary()
        if self.gravity:
            dict_space['gravity'] = self.gravity.dictionary()
        if self.wind:
            dict_space['wind'] = self.wind.dictionary()
        if self.lattice:
            dict_space['lattice'] = self.lattice.dictionary()
        if self.walls:
            dict_space['walls'] = self.walls.dictionary()

        return dict_space

    def set_dimension(self, dimension):
        self.dimension = dimension

    def add_particles(self, number, position=None):
        if not self.particles:
            self.particles = Particles()
            self.particles.dimension = self.dimension
        self.particles.add(number=number, position=position)

    def simulate(self, n=1, info=True, timer=None, save_particles=True, step_particles_insertion=0):
        """ Simulation function.
            n - number of iterations (integer), r - check furthest sensation distances (boolean),
            info - simulation information (boolean), timer - (None/object)"""

        for i in range(n):

            if save_particles:
                self.particles.save(project_id=self.project_id, simulation_number=self.simulation_number)

            if timer:
                timer.update(attribute=timer.simulation, action='start')

            if step_particles_insertion:
                self.particles.add(number=step_particles_insertion, position=[0,0,0])
                # self.particles.add(number=step_particles_insertion, position=[3,3,0])
                # self.particles.add(number=step_particles_insertion, position=[-6, 6, 0])

            self.particles.new_position(wind=self.wind, gravity=self.gravity, walls=self.walls)

            self.simulation_number += 1

            if timer:
                timer.update(attribute=timer.simulation, action='stop')

            if info:
                print(str(round((i + 1) * 100 / n, 2)) + ' %')

        if save_particles:
            self.particles.save(project_id=self.project_id, simulation_number=self.simulation_number)

    def save(self):
        if not os.path.exists('Dataset/Space/'+ project_id):
            os.makedirs('Dataset/Space/' + project_id)
        pickle.dump(self, open('Dataset/Space/' + self.project_id + '/' + str(self.simulation_number), 'wb'))

    @staticmethod
    def load(project_id = str(), simulation_number=None):
        saved_space = pickle.load(open('Dataset/Space/' + project_id + '/' + str(simulation_number), 'rb'), encoding='latin1')
        return saved_space


if __name__ == '__main__':
    project_id = str(0)

    space = Space(project_id=project_id)
    space.set_dimension(dimension=2)
    space.add_particles(number=int(1e5))
    space.simulate()
    space.save()
    print(space.dictionary())

    space = None
    space = Space.load(project_id = project_id, simulation_number=1)
    print(type(space))
    print(space.dictionary())