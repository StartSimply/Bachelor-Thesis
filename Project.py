import pickle, json, numpy, os
from Lattice import Lattice
from Visualisation import Visualiser
from Space import Space
from Timer import Timer
from Particles import Particles
from collections import OrderedDict
from Wall import Walls
from Wind import Wind


class CoreFunctions(object):

    def simulate(self, project_id=str(), load=False, save=True, number_of_iterations=int(), number_of_particles=int(), dimension=int()):
        info = dict()
        load_and_continue = load

        space = Space(project_id=project_id)
        timer = Timer()
        timer.start()

        # Pokracuj od poslednej ulozenej polohy castic
        if load_and_continue:
            info = json.load(open(project_id, 'r'))
            space.particles = Particles.load(project_id=info['project_id'], simulation_number=info['simulation_number'])
            space.set_dimension(dimension=info['dimension'])
            space.simulation_number = info['simulation_number']

        # Novy projekt
        if not load_and_continue:
            info = dict()
            info['number_of_particles'] = int(number_of_particles)
            info['dimension'] = dimension
            info['project_id'] = project_id
            # info['multisource'] = True
            # info['sources_distance'] = 10
            # info['particle_insertion'] = {'start': 0, 'end': 499, 'number': 200, 'position':[5,0,0]}

            space.set_dimension(dimension=info['dimension'])

            space.add_particles(number=int(info['number_of_particles']), position=[-5, -2, 0])

            space.walls = Walls()
            space.walls.add(x= -15, x_orientation=-1)
            space.walls.add(x= 15, x_orientation=1)
            space.walls.add(y= 15, y_orientation=1)
            space.walls.add(y= -15, y_orientation=-1)

            # space.wind = Wind()
            # space.wind.set(y_axis=1,x_axis=1, amplitude=0.05)
            # space.add_particles(number=int(info['number_of_particles']), position=[-3, -3, 0])
            # space.add_particles(number=int(info['number_of_particles']), position=[3, 3, 0])
            # space.add_particles(number=int(info['number_of_particles']), position=[-6, 6, 0])
            # space.add_particles(number=int(info['number_of_particles'])*10, position=[6, -6, 0])
            space.project_id = project_id
        # diffusion.space.wind.activate(wind_type='ConstantWind')
        # diffusion.space.wind.active_types['ConstantWind'].set(x_axis=5, amplitude=0.1)
        #
        # diffusion.space.walls.add()
        # diffusion.space.walls.pole[0].set(x_min=30, x_max=int(1e6))

        # Core functionality - simulation with saving particles
            self.save_lattice(project_id=project_id, particles=space.particles, simulation_number=space.simulation_number)

        if save:
            space.simulate(n=number_of_iterations, timer=timer)
        if not save:
            for i in range(number_of_iterations):
                print(i)
                # if i < 500:
                #     space.simulate(n=1, timer=timer, save_particles=False, step_particles_insertion=500)
                # else:
                #     if i == 500:
                #         space.wind = None
                space.simulate(n=10, timer=timer, save_particles=False, step_particles_insertion=0)
                self.save_lattice(project_id=project_id, particles=space.particles, simulation_number=space.simulation_number)

        info['simulation_number'] = space.simulation_number

        print(info)
        # Saving last state
        json.dump(info, open(project_id, 'w'))

        # Just final info
        timer.stop()
        print(timer)

    def save_lattice(self, project_id=str(), particles=None, simulation_number=int()):
        info = dict()
        info = json.load(open(project_id, 'r'))

        space = Space(project_id=project_id)
        space.lattice = Lattice()

        if particles:
            lattice = Lattice()
            lattice.update(particles=particles)
            lattice.save(project_id=project_id, simulation_number=simulation_number)

        else:
            i = 0
            while True:
                if os.path.exists('Dataset/Particles/' + project_id + '/' + str(i)):

                    print(str(i))

                    space.particles = Particles.load(project_id=info['project_id'], simulation_number=i)

                    space.lattice.update(particles=space.particles)

                    space.lattice.save(project_id=info['project_id'], simulation_number=i)

                    i += 1

                else:
                    break

    def inspect_lattice(self, project_id=str(), critical_concentration=None):

        info = dict()
        info = json.load(open(project_id, 'r'))

        lattice = Lattice()
        lattice.critical_concentration = int(1e5) * critical_concentration

        i = 0
        while True:
            if os.path.exists('Dataset/Lattices/' + project_id + '/' + str(i)):
                print(str(i))

                # loading state
                lattice.cells = Lattice.load(cells_only=True, project_id=project_id, simulation_number=i)

                # inspecting loaded state
                lattice.update_critical()

                lattice.sort_critical()
                lattice.update_maximal_distances(dimension=info['dimension'])

                i += 1

            else:
                break

        json.dump(lattice.maximal_distances, open(
            'Dataset/Maximal_distances/' + info['project_id'] + '/' + str(critical_concentration),
            'w'))

        # Visualiser.plot_scatter_2d(x=[particle.position.x_axis for particle in space.particles.pole],
        #                            y=[particle.position.y_axis for particle in space.particles.pole])

    @staticmethod
    def visualise(project_id=str(), max_distance=False, critical_concentration=None,
                  heatmap=False, simulation_number=str(), concentration=False):

        if max_distance:
            maximal_distances = json.load(
                open('Dataset/Maximal_distances/' + str(project_id) + '/' + str(critical_concentration),
                     'r'))
            Visualiser.plot_scatter_2d(x=numpy.arange(len(maximal_distances['concentrated'])),
                                       y=maximal_distances['concentrated'],
                                       project_id=project_id,
                                       info=str(critical_concentration)
                                       )

        if heatmap:
            info = json.load(open(project_id, 'r'))
            lattice = Lattice.load(project_id=project_id, simulation_number=simulation_number)
            print(lattice.cells)
            # critical_concentration = str(critical_concentration)

            if critical_concentration:
                Visualiser.concentration_heatmap(lattice=lattice, simulation_number=simulation_number,
                                             critical_concentration=critical_concentration)
            else:
                Visualiser.concentration_heatmap(lattice=lattice, simulation_number=simulation_number)
        if concentration:
            data = []
            # for simulation_number in [50, 100, 150, 300, 400, 450, 499]:
            # for simulation_number in [50, 100, 150, 200, 250, 300, 350, 400, 450, 499]:
            info = json.load(open(project_id, 'r')),
            lattice = Lattice.load(project_id=project_id, simulation_number=str(300))

            # lattice.critical_concentration = 3500
            # lattice.update_critical()

            val = dict()
            for cell in lattice.cells.values():
                val[cell.index.x_axis] = cell.get_concentration()
            od = OrderedDict(sorted(val.items()))
            x=[]
            y=[]
            for key, val in od.items():
                x.append(key)
                y.append(val)
            # if x or y:
            #     x.insert(0,x[0])
            #     y.insert(0,0)
            #     x.append(x[-1])
            #     y.append(0)
            data.append([x,y,simulation_number])
            Visualiser.plot_scatter_2d(data=data,
                                       project_id=project_id)


class Project(object):

    def __init__(self):
        self.id = str()
        self.functions = CoreFunctions()

    def set_id(self, id):
        self.id = id
        if not os.path.exists(id):
            os.makedirs('Dataset/Particles/'+ id)
            os.makedirs('Dataset/Lattices/' + id)
            os.makedirs('Dataset/Maximal_distances/' + id)
            json.dump('', open(id, 'w'))

    def run(self):
        # Pre zakomentovanie prikazu a teda neaktivitu danej funkcie umiestnite pred dany prikaz mriezku
        # Pre editaciu parametrov editujte priamo vybranu funkciu


        self.simulate()

        # self.create_lattice()

        # for concentration in [0.0001, 0.0005, 0.001, 0.0015, 0.002]:
        #     self.update_lattices(critical_concentration=concentration)
        #     self.visualise(critical_concentration=concentration)
        # for i in range(1,499,20):
        # self.visualise(heatmap=False, concentrated_range=True, simulation_number=i, critical_concentration=120)

    def simulate(self, load_particles = False, save_particles = False,
                   number_of_iterations = int(150),
                   number_of_particles = int(5e5), dimension = int(2)):

        f = CoreFunctions()

        # Pre nacitanie castic a pokracovani v iteracii z posledneho ulozeneneho stavu castic nastav 'True'
        load_particles = load_particles

        # Pre ukladanie castic pocas simulacie nastav 'True'
        # Pri neukladani castic bude automaticky priamo kalkulovana mriezka a nasledne ukladana iba ona samotna
        save_particles = save_particles

        # Nastavenie poctu iteracii
        number_of_iterations = number_of_iterations

        if not load_particles:
            # Nastavenie poctu castic
            number_of_particles = number_of_particles

            # Nastavenie dimenzie
            dimension = dimension

            f.simulate(project_id=self.id, load=False, save=save_particles, dimension=dimension,
                                   number_of_iterations=number_of_iterations, number_of_particles=number_of_particles)

        if load_particles:
            f.simulate(project_id=self.id, load=True, save=save_particles,
                                   number_of_iterations=number_of_iterations)

        # Pre nastavenie dalsich parametrov edituj priamo modul 'CoreFunctions'
        pass

    def create_lattice(self):

        # Vytvorenie novych vseobecnych mriezok
        self.functions.save_lattice(project_id=self.id)

        pass

    def update_lattices(self, critical_concentration = float()):

        # Nastavenie kritickej koncentracie
        critical_concentration = critical_concentration
        self.functions.inspect_lattice(project_id=self.id, critical_concentration=critical_concentration)

        pass

    def visualise(self, concentrated_range=False, critical_concentration=float(),
                        concentration = False, simulation_number = int(), heatmap=False):
        # Vizualizácia polomeru kriticky koncentrovanej oblasti
        if concentrated_range:
            CoreFunctions.visualise(project_id=self.id,
                                    max_distance=True,
                                    critical_concentration=critical_concentration)

        if concentration:
            CoreFunctions.visualise(project_id=self.id, concentration=True,
                                    simulation_number=str(simulation_number))
        if heatmap:
            CoreFunctions.visualise(project_id=self.id, heatmap=True,
                                    simulation_number=str(simulation_number),
                                    critical_concentration=critical_concentration)
        pass


if __name__ == '__main__':

    project = Project()

    # Zadanie id projektu
    project.set_id(str(21))

    # Pre vyber aktivnych funkcii editujte priamo funkciu run()
    # for i in range(3):
    #     n = [100, 1000, 10000]
    #     project.set_id(str(7+i))
    project.run()
