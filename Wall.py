class Walls(object):
    def __init__(self):
        self.pole = []

    def add(self, x=None, y=None, x_orientation=1, y_orientation=1):
        new_wall = Wall()
        new_wall.x_axis = x
        new_wall.y_axis = y
        new_wall.x_orientation = x_orientation
        new_wall.y_orientation = y_orientation
        self.pole.append(new_wall)


class Wall(object):

    def __init__(self):
        self.x_axis = None
        self.y_axis = None
        self.x_orientation = 1
        self.y_orientation = 1

