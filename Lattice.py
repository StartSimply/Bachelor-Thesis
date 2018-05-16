from math import floor, sqrt, pi, sin, cos
import pickle
import numpy
from collections import OrderedDict
import os
from Vector import Vector


class Lattice(object):

    def __init__(self):
        self.density = 1
        self.conditioned_neighbours = 2
        self.critical_concentration = float()

        self.cells = {}
        self.critical_cells = {}

        self.maximal_distances = {'concentrated': [], 'non_empty': []}

        self.boundaries = {'minimal': Vector(), 'maximal': Vector()}

    def __repr__(self):
        grid_lattice_repr = self.dictionary()
        return grid_lattice_repr

    def dictionary(self):
        lattice_dict = dict()
        lattice_dict['density'] = self.density
        lattice_dict['cells'] = {}
        for index, cell in self.cells.items():
            lattice_dict['cells'][index] = cell.dictionary()

        return lattice_dict

    def save(self, project_id=str(), sub_id= str(), simulation_number=None, implementation=False):
        if implementation:
            if not os.path.exists(project_id + '/Lattices'):
                os.makedirs(project_id + '/Lattices')
            pickle.dump(self.dictionary(), open(project_id + sub_id + '/Lattices/' + str(simulation_number), 'wb'))
        else:
            if not os.path.exists('Dataset/Lattices/' + project_id):
                os.makedirs('Dataset/Lattices/' + project_id)
            pickle.dump(self.dictionary(), open('Dataset/Lattices/' + project_id +'/'+ str(simulation_number), 'wb'))

    @staticmethod
    def load(cells_only=None, project_id=str(), sub_id = '', simulation_number=None, implementation=False):
        if implementation:
            saved_lattice=pickle.load(open(str(project_id) + sub_id + 'Lattices/' + str(simulation_number), 'rb'))
        else:
            saved_lattice = pickle.load(open('Dataset/Lattices/' + str(project_id) +'/'+ str(simulation_number), 'rb'))
        loaded_lattice = Lattice()
        loaded_lattice.density = saved_lattice['density']

        for index, saved_cell in saved_lattice['cells'].items():
            loaded_lattice.cells[index] = Cell.load(saved_cell=saved_cell)

        if cells_only:
            return loaded_lattice.cells

        return loaded_lattice

    def set_critical_concentration(self, critical_value):
        self.critical_concentration = critical_value

    def set_density(self, density):
        self.density = density

    def interval(self):
        interval = 1 / self.density
        return interval

    def initialize_sections(self, cells=True, critical_cells=True):
        if cells:
            self.cells = {}
        if critical_cells:
            self.critical_cells = {}

    def update(self, particles):
        self.cells = {}

        for particle in particles.pole:
            cell_index = Vector().create()
            cell_index.x_axis = floor(particle.position.x_axis * self.density)
            cell_index.y_axis = floor(particle.position.y_axis * self.density)
            cell_index.z_axis = floor(particle.position.z_axis * self.density)
            index_key = self.get_index_key(cell_index=cell_index)
            if self.cells.get(index_key):
                self.cells[index_key].counter += 1
            else:
                section = Cell(index=cell_index)
                self.cells[index_key] = section

    def update_critical(self):
        self.critical_cells = {}

        if self.critical_concentration:
            for index, cell in self.cells.items():
                if cell.get_concentration() >= self.critical_concentration:
                    self.critical_cells[index] = cell

    def sort_critical(self):
        if self.critical_cells:
            amplitudes_dict = {}
            for critical_cell in self.critical_cells.values():
                position = critical_cell.position(interval_size=self.interval())
                amplitude = position.get_amplitude()
                if amplitudes_dict.get(position.get_amplitude()):
                    amplitudes_dict[amplitude].append(critical_cell)
                else:
                    amplitudes_dict[amplitude] = [critical_cell]
            sorted_amplitudes = sorted(amplitudes_dict)

            sorted_critical_cells = OrderedDict()
            for amplitude in reversed(sorted_amplitudes):
                for critical_cell in amplitudes_dict[amplitude]:
                    sorted_critical_cells[self.get_index_key(cell_index=critical_cell.index)] = critical_cell

            self.critical_cells = sorted_critical_cells

    @staticmethod
    def get_index_key(cell_index=None):
        index_key = str([cell_index.x_axis, cell_index.y_axis, cell_index.z_axis])
        return index_key

    def update_maximal_distances(self, dimension=int(), check_area=True):
        self.sort_critical()

        if self.critical_concentration and self.critical_cells:
            self.maximal_distances['concentrated'].append(self.get_maximal_distance(dimension=dimension, check_area=check_area))
        else:
            print('not updating maximal distances')
            self.maximal_distances['concentrated'].append(0)

    def get_maximal_distance(self, dimension=int(), check_area=True):

        maximal_distance = 0

        if check_area:
            critical_area = len(self.critical_cells) * (self.interval() ** dimension)
            min_rate = 0.75

        cycle = 0

        for cell in self.critical_cells.values():
            section_approved = True
            section_distance = cell.position(interval_size=self.interval()).get_amplitude()

            if self.conditioned_neighbours:
                section_approved = False
                cell_neighbours = self.count_adjacent_cells(cell=cell, cells=self.critical_cells)
                if cell_neighbours >= self.conditioned_neighbours:
                    section_approved = True

            if check_area:
                section_approved = False
                area = critical_area - cycle * (self.interval() ** dimension)

                if dimension == 2:
                    radial_area = (section_distance ** 2) * numpy.pi
                if dimension == 3:
                    raise ValueError

                rate = area / radial_area
                if rate >= min_rate:
                    section_approved = True

            if section_approved:
                maximal_distance = section_distance
                break

            cycle += 1

        return maximal_distance

    def count_adjacent_cells(self, cell, cells):
        counter = 0
        dimension = 2

        if dimension >= 1:
            clone_cell = cell.clone()
            clone_cell.index.x_axis += 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

            clone_cell = cell.clone()
            clone_cell.index.x_axis -= 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

        if dimension >= 2:
            clone_cell = cell.clone()
            clone_cell.index.y_axis += 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

            clone_cell = cell.clone()
            clone_cell.index.y_axis -= 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

        if dimension == 3:
            clone_cell = cell.clone()
            clone_cell.index.z_axis += 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

            clone_cell = cell.clone()
            clone_cell.index.z_axis -= 1
            if self.get_index_key(cell_index=clone_cell.index) in cells.keys():
                counter += 1

        return counter

    def update_boundaries(self):
        cells = self.cells
        for cell in cells.values():
            if cell.index.x_axis < self.boundaries.get('minimal').x_axis:
                self.boundaries.get('minimal').x_axis = cell.clone().index.x_axis
            elif cell.index.x_axis > self.boundaries.get('maximal').x_axis:
                self.boundaries.get('maximal').x_axis = cell.clone().index.x_axis
            if cell.index.y_axis < self.boundaries.get('minimal').y_axis:
                self.boundaries.get('minimal').y_axis = cell.clone().index.y_axis
            elif cell.index.y_axis > self.boundaries.get('maximal').y_axis:
                self.boundaries.get('maximal').y_axis = cell.clone().index.y_axis
            if cell.index.z_axis < self.boundaries.get('minimal').z_axis:
                self.boundaries.get('minimal').z_axis = cell.clone().index.z_axis
            elif cell.index.z_axis > self.boundaries.get('maximal').z_axis:
                self.boundaries.get('maximal').z_axis = cell.clone().index.z_axis


class Cell(object):

    def __init__(self, index=None, counter=1):
        self.index = index
        self.counter = counter

    def __repr__(self):
        cell_repr = str(self.dictionary())
        return cell_repr

    def position(self, interval_size):
        position = Vector()
        position.x_axis = (self.index.x_axis + 0.5) * interval_size
        position.y_axis = (self.index.y_axis + 0.5) * interval_size
        position.z_axis = 0
        return position

    def clone(self):
        clone = Cell(index=self.index.clone(), counter=self.counter)
        return clone

    def dictionary(self):
        section_dict = {'counter': self.counter,
                        'index': self.index.dictionary()
                        }
        return section_dict

    def get_concentration(self):
        concentration = self.counter
        return concentration

    @staticmethod
    def load(saved_cell=None):
        loaded_cell = Cell()
        loaded_cell.index = Vector.load(saved_vector=saved_cell['index'])
        loaded_cell.counter = saved_cell['counter']
        return loaded_cell


if __name__ == '__main__':

    pass


