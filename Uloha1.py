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

# Jednorazový lokalizovaný zdroj v dvoch rozmeroch


class JednorazovyZdroj(object):

    def __init__(self):
        self.id = 'implementation1'
        self.sub_id = '/project2/'
        self.dimension = 2
        self.number_of_particles = int(5e5)
        self.number_of_iterations = int(750)

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

        space.simulate(n=self.number_of_iterations, timer=timer)

        info['simulation_number'] = space.simulation_number

        timer.stop()

        info['timer'] = timer.dictionary()
        json.dump(info, open(str(self.id) + '/' + 'info', 'w'))

        print(info)

    def create_lattice(self):
        info = dict()
        info = json.load(open(str(self.id) + self.sub_id + '/' + 'info', 'r'))

        lattice = Lattice()
        lattice.density = 1
        i = 0
        while True:
            if os.path.exists(self.id + self.sub_id + '/Particles/' + str(i)):

                print(str(i))

                particles = Particles.load(project_id=self.id, sub_id=self.sub_id, simulation_number=i, implementation=True)

                lattice.update(particles=particles)

                lattice.save(project_id=self.id, sub_id = self.sub_id, simulation_number=i, implementation=True)

                i += 1

            else:
                break

    def inspect_lattice(self, critical_concentration):
        info = dict()
        info = json.load(open(str(self.id) + self.sub_id +'/' + 'info', 'r'))

        lattice = Lattice()
        lattice.critical_concentration = info['number_of_particles'] * critical_concentration

        i = 0
        while True:
            if os.path.exists(self.id + self.sub_id + '/Lattices/' + str(i)+ 'L1'):
                print(str(i))

                lattice.cells = Lattice.load(cells_only=True, project_id=self.id, simulation_number=i, implementation=True)

                lattice.update_critical()

                lattice.update_maximal_distances(dimension=info['dimension'])

                i += 1

            else:
                break

        json.dump(lattice.maximal_distances['concentrated'], open(self.id + self.sub_id +'/Maximal_distances/' + str(critical_concentration)+'n2A', 'w'))

    def visualise(self, heatmap=False, max_distance=False, critical_concentration=float(), simulation_number=None):

        if heatmap:
            lattice = Lattice.load(project_id=self.id, sub_id=self.sub_id, simulation_number=simulation_number, implementation=True)
            print(lattice.dictionary())
            Visualiser.concentration_heatmap(lattice=lattice,
                                             simulation_number=simulation_number,
                                             critical_concentration=critical_concentration)

        # if heatmap:
        #     x_max = 80
        #     x_min = -80
        #     y_max = 0
        #     y_min = 0
        #
        #     fig = tools.make_subplots(rows=7, cols=1, print_grid=False)
        #
        #     y_size = int((y_max - y_min)) + 1
        #     x_size = int((x_max - x_min)) + 1
        #     data = np.zeros((y_size, x_size))
        #
        #     for i in range(50,700,100):
        #         lattice = Lattice.load(project_id=self.id, sub_id=self.sub_id, simulation_number=i, implementation=True)
        #
        #         for cell in lattice.cells.values():
        #             if cell.get_concentration() > critical_concentration:
        #                 if cell.position(1).x_axis > x_min and cell.position(1).x_axis < x_max:
        #                     data[int((cell.index.y_axis - y_min)), int((cell.index.x_axis - x_min))] = cell.counter
        #
        #         graph_x_axis = list(range(int(x_min * lattice.density), int(x_max * lattice.density)))
        #         graph_y_axis = list(range(int(y_min * lattice.density), int(y_max * lattice.density)))
        #
        #     # colorscale = [
        #     #     [0, 'rgb(0, 0, 0)'],
        #     #     [0.1, 'rgb(0, 0, 0)'],
        #     #     [0.1, 'rgb(20, 20, 20)'],
        #     #     [0.2, 'rgb(20, 20, 20)'],
        #     #     [0.2, 'rgb(40, 40, 40)'],
        #     #     [0.3, 'rgb(40, 40, 40)'],
        #     #
        #     #     [0.3, 'rgb(60, 60, 60)'],
        #     #     [0.4, 'rgb(60, 60, 60)'],
        #     #
        #     #     [0.4, 'rgb(80, 80, 80)'],
        #     #     [0.5, 'rgb(80, 80, 80)'],
        #     #
        #     #     [0.5, 'rgb(100, 100, 100)'],
        #     #     [0.6, 'rgb(100, 100, 100)'],
        #     #
        #     #     [0.6, 'rgb(120, 120, 120)'],
        #     #     [0.7, 'rgb(120, 120, 120)'],
        #     #
        #     #     [0.7, 'rgb(140, 140, 140)'],
        #     #     [0.8, 'rgb(140, 140, 140)'],
        #     #
        #     #     [0.8, 'rgb(160, 160, 160)'],
        #     #     [0.9, 'rgb(160, 160, 160)'],
        #     #
        #     #     [0.9, 'rgb(180, 180, 180)'],
        #     #     [1.0, 'rgb(180, 180, 180)']]
        #         trace = go.Heatmap(z=data, x=graph_x_axis, y=graph_y_axis)
        #         fig.append_trace(trace, int(i/100+0.5), 1)
        #         # , colorscale=colorscale)
        #
        #     layout = go.Layout(title='Rozloženie koncentrácie pre 1D prípad',
        #                        xaxis=dict(title='Priestorová súradnica x'),
        #                                   # titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
        #                        yaxis=dict(title='y = 0'),)
        #                                   # titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        #
        #
        #     fig['layout'].update(height=1000, width=1000, title='Multiple Subplots')
        #     # fig = go.Figure(data=plot_data, layout=layout)
        #     plotly.offline.plot(fig, filename='H'+str(simulation_number)+'.html',
        #                     image_filename='h'+str(simulation_number), image_width=800, image_height=800, image='png',
        #                     auto_open=True)
        #     # Visualiser.concentration_heatmap(lattice=lattice, simulation_number=simulation_number, critical_concentration=critical_concentration)

        if max_distance:
            maximal_distances = json.load(open(str(self.id) + self.sub_id + '/Maximal_distances/' + str(critical_concentration)+'n2A',
                     'r'))
            print(maximal_distances)
            trace = go.Scatter(
                    x=np.arange(len(maximal_distances)),
                    y=maximal_distances,
                    mode='lines+markers',
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
            plotly.offline.plot(fig, filename='impl1-2D-1e5-R(n)'+ str(critical_concentration)+'n2A' +'.html')





if __name__ == '__main__':

    implementation = JednorazovyZdroj()

    # implementation.create_data()

    # implementation.create_lattice()

    # for i in [0.0005,0.0008,0.001,0.0012,0.0015]:
        # implementation.inspect_lattice(critical_concentration=i)

        # implementation.visualise(max_distance=True, critical_concentration=i)

    for i in range(50,751,100):
        implementation.visualise(heatmap=True, simulation_number=i, critical_concentration=int(1e5)*0.0020)
