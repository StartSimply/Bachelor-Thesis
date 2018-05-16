import numpy as np
import plotly
import plotly.graph_objs as go
from plotly import tools
from Lattice import Lattice


class Heatmap(object):

    def __init__(self):
        self.project_id = 18
        self.x_max = 30
        self.x_min = -30
        self.x_axis = list(range(int(self.x_min), int(self.x_max)))
        self.y_max = 40
        self.y_min = -20
        self.y_axis = list(range(int(self.y_min), int(self.y_max)))
        self.zmax = 700
        self.critical_c = 10
        self.colorscale1 = [
            [1, 'rgb(0, 0, 0)'],
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
        self.colorscale2 = [[0, 'rgb(244, 244, 244)'],
                            [0.0001, 'rgb(0, 0, 0)'],
                            [1, 'rgb(0, 0, 0)']]
        self.colorscale = self.colorscale2
        self.horizontal_spacing = 0.02
        self.vertical_spacing = 0.02

    def single(self, simulation_number=int()):
        data = self.get_data(simulation_number=simulation_number)
        trace = go.Heatmap(z=data, x=self.x_axis, y=self.y_axis, zauto=False, zmax=self.zmax, showscale=False, colorscale=self.colorscale)
        self.show(data=[trace],info=simulation_number)

    def animate(self):
        frames = []
        for i in range(1,499,35):
            data = self.get_data(simulation_number=i)
            trace = go.Heatmap(z=data, x=self.x_axis, y=self.y_axis, zauto=False, zmax=self.zmax, showscale=False,
                               colorscale=self.colorscale)
            frames.append({'data':[trace]})
        self.show(data=frames[0]['data'], frames=frames)

    def multiple(self):
        data = []
        for i in range(0,500,20):
            sub_data = self.get_data(simulation_number=i)
            trace = go.Heatmap(z=sub_data, x=self.x_axis, y=self.y_axis, zauto=False, zmax=self.zmax, showscale=False,
                               colorscale=self.colorscale)
            data.append(trace)
        fig = tools.make_subplots(rows=5, cols=5, shared_xaxes=True, shared_yaxes=True,
                                  horizontal_spacing=self.horizontal_spacing, vertical_spacing=self.vertical_spacing)
        for i in range(len(data)):
            fig.append_trace(data[i], i//5+1, i%5+1)
        self.show(fig=fig)

    def show(self, fig=None, data = list(), frames = list(), info = None):
        layout = go.Layout(
            xaxis=dict(title='x', titlefont=dict(size=24)),
            yaxis=dict(title='y', titlefont=dict(size=24)))
        if not fig:
            fig = go.Figure(data=data, layout=layout, frames=frames)
        plotly.offline.plot(fig, filename=str(self.project_id) + 'HeatMap' + str(info) + '.html',
                            image_filename=str(self.project_id) + 'HeatMap' + str(info), image = 'png', image_width=1000, image_height=1200, auto_open=True)

    def get_data(self, simulation_number=int()):
        data = np.zeros((int(self.y_max-self.y_min), int(self.x_max-self.x_min)))
        cells = Lattice.load(project_id=self.project_id, simulation_number=simulation_number, cells_only=True)
        for cell in cells.values():
            if cell.get_concentration() > self.critical_c:
                if cell.position(1).x_axis > self.x_min and cell.position(1).x_axis < self.x_max:
                    if cell.position(1).y_axis > self.y_min and cell.position(1).y_axis < self.y_max:
                        data[int((cell.index.y_axis-self.y_min)), int((cell.index.x_axis-self.x_min))] = cell.counter
        return data


if __name__ == '__main__':
    heatmap = Heatmap()

    # heatmap.single(simulation_number=100)

    heatmap.multiple()