import json, os
from Space import Space
from Timer import Timer
from Lattice import Lattice
from Particles import Particles
from Visualisation import Visualiser
import numpy as np
import plotly
import plotly.graph_objs as go
import time
from plotly import tools

# Kontinuálny lokalizovaný zdroj v dvoch rozmeroch


class KontinualnyZdroj(object):

    def __init__(self):
        self.id = 'implementation2'
        self.sub_id = '/project5/'
        self.dimension = 2
        self.number_of_particles = int(1e5)
        self.number_of_iterations = int(700)
        self.particle_insertion = {'start':0, 'end':499, 'number':250}

    def create_data(self):

        space = Space(project_id=self.id)
        timer = Timer()

        timer.start()

        info = dict()
        info['number_of_particles'] = int(self.number_of_particles)
        info['dimension'] = int(self.dimension)
        info['project_id'] = self.id

        space.set_dimension(dimension=info['dimension'])
        space.add_particles(number=int(info['number_of_particles']), position=[0, 0, 0])

        space.simulate(n=500, timer=timer, step_particles_insertion=self.particle_insertion.get('number'))
        space.simulate(n=200, timer=timer)

        info['simulation_number'] = space.simulation_number

        timer.stop()

        info['timer'] = timer.dictionary()
        json.dump(info, open(str(self.id) + '/' + 'info', 'w'))

        print(info)

    def create_lattice(self):
        info = dict()
        info = json.load(open(str(self.id) + self.sub_id + 'info', 'r'))

        lattice = Lattice()

        i = 0
        while True:
            if os.path.exists(self.id + self.sub_id + 'Particles/' + str(i)):

                print(str(i))

                particles = Particles.load(project_id=info['project_id'], simulation_number=i, implementation=True)

                lattice.update(particles=particles)

                lattice.save(project_id=info['project_id'], simulation_number=i, implementation=True)

                i += 1

            else:
                break

    def inspect_lattice(self, critical_concentration):
        info = dict()
        info = json.load(open(str(self.id) + self.sub_id + 'info', 'r'))

        lattice = Lattice()
        lattice.critical_concentration = critical_concentration

        i = 0
        while True:
            if os.path.exists(self.id + self.sub_id + 'Lattices/' + str(i)):
                print(str(i))

                lattice.cells = Lattice.load(cells_only=True, project_id=self.id, sub_id=self.sub_id,
                                             simulation_number=i, implementation=True)

                lattice.update_critical()

                lattice.update_maximal_distances(dimension=info['dimension'], check_area=False)

                i += 1

            else:
                break

        json.dump(lattice.maximal_distances['concentrated'], open(self.id + self.sub_id + 'Maximal_distances/' + str(critical_concentration)+'n2', 'w'))

    def visualise(self, heatmap=False, max_distance=False, critical_concentration=float(), simulation_number=None):

        if heatmap:
            x_max = 60
            x_min = -60
            y_max = 60
            y_min = -60

            y_size = int((y_max - y_min)) + 1
            x_size = int((x_max - x_min)) + 1
            data = np.zeros((y_size, x_size))
            plot_data = []
            for i in range(10,700,50):
                lattice = Lattice.load(project_id=self.id, sub_id=self.sub_id, simulation_number=i, implementation=True)

                for cell in lattice.cells.values():
                    if cell.get_concentration() > critical_concentration:
                        if cell.position(1).x_axis > x_min and cell.position(1).x_axis < x_max:
                            if cell.position(1).y_axis > y_min and cell.position(1).y_axis < y_max:
                                data[int((cell.index.y_axis - y_min)), int((cell.index.x_axis - x_min))] = cell.counter

                graph_x_axis = list(range(int(x_min * lattice.density), int(x_max * lattice.density)))
                graph_y_axis = list(range(int(y_min * lattice.density), int(y_max * lattice.density)))
                trace = go.Heatmap(z=data, x=graph_x_axis, y=graph_y_axis)
                plot_data.append(trace)

            fig = tools.make_subplots(rows=4, cols=4)
            for i in range(len(plot_data)):
                print(plot_data[i]['z'])
                # fig.append_trace(plot_data[i], i//4+1, i%4+1)
            # plotly.offline.plot(fig, filename='H' + str(simulation_number) + '.html',
            #                     image_filename='2D-h' + str(simulation_number) ,
            #                     image_width=800, image_height=800, image='png', auto_open=True)
            # Visualiser.concentration_heatmap(lattice=lattice, simulation_number=simulation_number, critical_concentration=critical_concentration)

        if max_distance:
            maximal_distances = json.load(open(str(self.id) + self.sub_id + 'Maximal_distances/' + str(critical_concentration)+'n2',
                     'r'))
            print(maximal_distances)
            trace = go.Scatter(
                    x=np.arange(len(maximal_distances)),
                    y=maximal_distances,
                    mode='markers',
                                )
            data = [trace]
            layout = go.Layout(
                title = '',
                xaxis=dict(
                    title='Počet iteračných krokov',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=14,
                        color='#7f7f7f')
                ),
                yaxis=dict(
                    title='Polomer oblasti s kritickou koncentráciou',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=14,
                        color='#7f7f7f')
                )
            )
            fig = go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig, filename='impl2-2D-1e5-R(n)'+ str(critical_concentration)+'n2' +'.html')





if __name__ == '__main__':

    implementation = KontinualnyZdroj()

    # implementation.create_data()

    # implementation.create_lattice()

    # for i in [0.0005,0.0008,0.001,0.0012,0.0015]:
        # implementation.inspect_lattice(critical_concentration=i*100000)

    implementation.visualise(max_distance=False, heatmap=True, simulation_number=400)
                             # , critical_concentration=i*100000)
        # implementation.visualise(max_distance=True, critical_concentration=i*100000, heatmap=True, simulation_number=600)