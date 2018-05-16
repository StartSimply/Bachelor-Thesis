import numpy as np
import plotly
import plotly.graph_objs as go
from plotly import tools


class Visualiser(object):

    @staticmethod
    def concentration_heatmap(lattice=None, critical_concentration=float(), fixed_size=True, simulation_number=None):
        cells = lattice.cells
        # colorscale = [
        #     [0, 'rgb(0, 0, 0)'],
        #     [0.1, 'rgb(0, 0, 0)'],
        #     [0.1, 'rgb(20, 20, 20)'],
        #     [0.2, 'rgb(20, 20, 20)'],
        #     [0.2, 'rgb(40, 40, 40)'],
        #     [0.3, 'rgb(40, 40, 40)'],
        #
        #     [0.3, 'rgb(60, 60, 60)'],
        #     [0.4, 'rgb(60, 60, 60)'],
        #
        #     [0.4, 'rgb(80, 80, 80)'],
        #     [0.5, 'rgb(80, 80, 80)'],
        #
        #     [0.5, 'rgb(100, 100, 100)'],
        #     [0.6, 'rgb(100, 100, 100)'],
        #
        #     [0.6, 'rgb(120, 120, 120)'],
        #     [0.7, 'rgb(120, 120, 120)'],
        #
        #     [0.7, 'rgb(140, 140, 140)'],
        #     [0.8, 'rgb(140, 140, 140)'],
        #
        #     [0.8, 'rgb(160, 160, 160)'],
        #     [0.9, 'rgb(160, 160, 160)'],
        #
        #     [0.9, 'rgb(180, 180, 180)'],
        #     [1.0, 'rgb(180, 180, 180)']]

        colorscale = [
            [0, 'rgb(0, 0, 0)'],
            [1/57.5, 'rgb(0, 0, 0)'],
            [1/57.5, 'rgb(20, 20, 20)'],
            [1/115, 'rgb(20, 20, 20)'],
            [1/115, 'rgb(40, 40, 40)'],
            [1/25, 'rgb(40, 40, 40)'],

            [1/25, 'rgb(60, 60, 60)'],
            [1/5, 'rgb(60, 60, 60)'],

            [1/5, 'rgb(80, 80, 80)'],
            [1/10, 'rgb(80, 80, 80)'],

            [1/10, 'rgb(100, 100, 100)'],
            [1/100, 'rgb(100, 100, 100)'],

            [1/100, 'rgb(120, 120, 120)'],
            [1/1000, 'rgb(120, 120, 120)'],

            [1/1000, 'rgb(140, 140, 140)'],
            [1/10000, 'rgb(140, 140, 140)'],

            [1/10000, 'rgb(160, 160, 160)'],
            [1/100000, 'rgb(160, 160, 160)'],

            [1/100000, 'rgb(180, 180, 180)'],
            [0, 'rgb(180, 180, 180)']]

        if not fixed_size:
            lattice.update_boundaries()
            x_max = lattice.boundaries.get('maximal').x_axis
            x_min = lattice.boundaries.get('minimal').x_axis
            y_max = lattice.boundaries.get('maximal').y_axis
            y_min = lattice.boundaries.get('minimal').y_axis

        else:
            x_max = 30
            x_min = -30
            y_max = 30
            y_min = -30

        y_size = int((y_max-y_min))
        x_size = int((x_max-x_min))
        data = np.zeros((y_size, x_size))

        for cell in cells.values():
            if cell.get_concentration()> critical_concentration:
                if cell.position(1).x_axis > x_min and cell.position(1).x_axis < x_max:
                    if cell.position(1).y_axis > y_min and cell.position(1).y_axis < y_max:
                        data[int((cell.index.y_axis-y_min)), int((cell.index.x_axis-x_min))] = cell.counter

        graph_x_axis = list(range(int(x_min), int(x_max)))
        graph_y_axis = list(range(int(y_min), int(y_max)))

        trace = go.Heatmap(z=data, x=graph_x_axis, y=graph_y_axis, zauto=False, zmax=500, colorscale=colorscale)
        plot_data = [trace]
        layout = go.Layout(
            title='Rozdelenie koncentrácie po ' + str(simulation_number) + ' iteračných krokoch' ,
            titlefont=dict(size=24),
                           xaxis=dict(title='x', titlefont=dict(family='Courier New, monospace', size=24)),
                           yaxis=dict(title='y', titlefont=dict(family='Courier New, monospace', size=24)))
        fig = go.Figure(data=plot_data, layout=layout)
        plotly.offline.plot(fig, filename='H'+str(simulation_number)+'.html',
                            image_filename='2D-h'+str(simulation_number)+'')
                            # image_width=800, image_height=800, image='png', auto_open=True)

    @staticmethod
    def plot_scatter_2d(data=None, project_id=None, info=None):
        print(data)
        plot_data = []
        for item in data:
            trace = go.Scatter(
                x=item[0],
                y=item[1],
                mode='none',
                fill = 'tozeroy',
                name= 'N = ' + str(item[2]) + ' krokov'
            )
            plot_data.append(trace)
        layout = go.Layout(
            # title='Zobrazenie koncentrácie >= pre 1D prípad v rôznych časoch',
            xaxis=dict(
                title='Priestorová súradnica',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=14,
                    color='#7f7f7f')
            ),
            yaxis=dict(
                title='Koncentrácia',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=14,
                    color='#7f7f7f')
            )
        )
        fig = go.Figure(data=plot_data, layout=layout)
        plotly.offline.plot(fig, filename='plot-1D'+ str(project_id) +'.html')


if __name__ == '__main__':

    pass
