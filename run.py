import pickle, json, numpy, os
from Lattice import Lattice
from Visualisation import Visualiser
from Space import Space
from Timer import Timer
from Particles import Particles
from collections import OrderedDict
from Wall import Walls
from Wind import Wind
from Vector import Vector
from HeatMap import Heatmap

class Simulator(object):

    def __init__(self):
        self.id = '0'
        self.set_id()
        self.dimension = int(2)
        self.number_of_iterations = int(100)
        self.sources = []

    def set_id(self):
        if not os.path.exists('Dataset'):
            os.makedirs('Dataset')
            os.makedirs('Dataset/Lattices')
        project_id = '0'
        while os.path.exists('Dataset/Lattices/' + project_id):
            project_id = str(int(project_id) + 1)
        self.id = project_id
        os.makedirs('Dataset/Lattices/' + self.id)

    def set_parameters(self):
        edit = input('Chcete zmenit prednastavene parametre? y/n \n')
        if edit == 'y':
            self.dimension = int(input('Zadajte pocet dimenzii. (1, 2, 3) \n'))
            self.number_of_iterations = int(input('Zadajte pocet iteracii simulacie. \n'))
            self.add_sources()
            print('Zakladne parametre boli nastavene.')
        else:
            one_source = Source()
            self.sources.append(one_source)
            print('Prednastavene parametre boli prijate ako nastavenie simulacie.')

    def add_sources(self):
        edit1 = input('Chcete editovat prednastaveny zdroj aromatickych castic? y/n \n')
        if edit1 == 'y':
            number_of_sources = int(input('Zadajte pocet zdrojov castic. \n'))
            for i in range(number_of_sources):
                new_source = Source()
                change_parameters = input('Chcete zmenit povodne nastavenia pre zdroj'+str(i)+'? y/n \n')
                if change_parameters == 'y':
                    position_x = float(input('Zadajte x-ovu suradnicu. \n'))
                    position_y = float(input('Zadajte y-ovu suradnicu. \n'))
                    position_z = float(input('Zadajte z-ovu suradnicu. \n'))
                    new_source.position = Vector.list_input(position_list=[position_x, position_y, position_z])
                    new_source.initial_particles_N = int(input('Zadajte pocet castic vypustenych zdrojom '+str(i)+' pri inicializacii systemu. \n'))
                    new_source.insertion = int(input('Zadajte pocet castic vypustanych zdrojom '+str(i)+' v kazdom kroku simulacie. \n'))
                self.sources.append(new_source)
                print('Novy zdroj pridany. \n')
        else:
            new_source = Source()
            self.sources.append(new_source)
            print('Vlozeny prednastaveny zdroj aromatickych castic. \n')

    def simulate(self):

        space = Space(project_id=self.id)
        timer = Timer()
        timer.start()

        space.set_dimension(dimension=self.dimension)
        for source in self.sources:
            space.add_particles(number=int(source.initial_particles_N),
                                position=[source.position.x_axis,source.position.y_axis, source.position.z_axis])

        for i in range(int(self.number_of_iterations / 25)):
            space.simulate(n=25, info=True, timer=timer, save_particles=False, sources=self.sources)
            self.save_lattice(particles=space.particles, simulation_number=space.simulation_number)

        timer.stop()
        print(timer.dictionary())

    def save_lattice(self, particles=None, simulation_number=int()):

        lattice = Lattice()
        lattice.update(particles=particles)
        lattice.save(project_id=self.id, simulation_number=simulation_number)
        print('Aktualny stav koncentracie ulozeny. Cislo iteracie = ' + str(simulation_number))

    def visualise(self):

        heatmap = Heatmap()
        heatmap.project_id = self.id
        heatmap.x_max = 30
        heatmap.x_min = -30
        heatmap.y_max = 30
        heatmap.y_min = -30
        heatmap.critical_c = 0
        heatmap.colorscale = heatmap.colorscale1

        heatmap.multiple()

        if input('Chcete zadat kriticku koncentraciu a zobrazit nadkriticku oblast? y/n \n') == 'y':
            heatmap.critical_c = int(input('Zadajte kriticku koncentraciu. \n'))
            heatmap.colorscale = heatmap.colorscale2
            heatmap.multiple()
            heatmap.critical_c = 0
            heatmap.colorscale = heatmap.colorscale1

        if input('Chcete zobrazit animaciu? y/n \n') == 'y':
            heatmap.animate()

    def run(self):

        self.set_parameters()

        self.simulate()

        self.visualise()

        print('V pripade ak chcete preskumat ulozene koncentracne mriezky, pouzite modul Heatmap. \n')


class Source(object):

    def __init__(self):
        self.position = Vector.list_input(position_list=[0,0,0])
        self.initial_particles_N = int(1e5)
        self.insertion = int(250)


if __name__ == '__main__':

    simulation = Simulator()
    simulation.run()