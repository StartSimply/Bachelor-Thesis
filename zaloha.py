@staticmethod
def plot_scatter_2d(data=None, project_id=None, info=None):
    print(data)
    plot_data = []
    for item in data:
        trace = go.Scatter(
            x=item[0],
            y=item[1],
            mode='none',
            fill='tozeroy',
            name='N = ' + str(item[2]) + ' krokov'
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
    plotly.offline.plot(fig, filename='plot-1D-1.html')


if heatmap:
    x_max = 60
    x_min = -60
    y_max = 60
    y_min = -60

    y_size = int((y_max - y_min)) + 1
    x_size = int((x_max - x_min)) + 1
    data = np.zeros((y_size, x_size))
    plot_data = []
    for i in range(10, 700, 60):
        lattice = Lattice.load(project_id=self.id, sub_id=self.sub_id, simulation_number=simulation_number,
                               implementation=True)

        for cell in lattice.cells.values():
            if cell.get_concentration() > critical_concentration:
                data[int((cell.index.y_axis - y_min)), int((cell.index.x_axis - x_min))] = cell.counter

        graph_x_axis = list(range(int(x_min * lattice.density), int(x_max * lattice.density)))
        graph_y_axis = list(range(int(y_min * lattice.density), int(y_max * lattice.density)))
        trace = go.Heatmap(z=data, x=graph_x_axis, y=graph_y_axis)
        plot_data.append(trace)

    fig = tools.make_subplots(rows=14, cols=1)
    for i in range(len(plot_data)):
        fig.append_trace(plot_data[i], i + 1, 1)

        # Visualiser.concentration_heatmap(lattice=lattice, simulation_number=simulation_number, critical_concentration=critical_concentration)