import time


class Timer(object):

    def __init__(self):
        self.processing = {'start': float(), 'end': float(), 'total_time': float()}
        self.simulation = {'start': float(), 'end': float(), 'total_time': float()}
        self.running = False
        self.approximation_constant = 1/1e6
        self.start()

    def __repr__(self):
        simulation = 'simulation ' + str(self.simulation['total_time']) + '\n'
        processing = 'processing ' + str(self.processing['total_time']) + '\n'

        timer_repr = simulation + processing
        return timer_repr

    def start(self):
        self.running = True
        self.update(attribute=self.processing, action='start')

    def stop(self):
        self.running = False
        self.update(attribute=self.processing, action='stop')
        if self.simulation.get('start'):
            self.update(attribute=self.simulation, action='stop')

    def reset(self):
        if self.running:
            self.stop()
        attributes = [self.processing, self.simulation]
        for attribute in attributes:
            self.update(attribute=attribute, action='reset')

    def update(self, attribute, action):
        if action == 'start':
            attribute['start'] = time.time()

        elif action == 'stop':
            attribute['end'] = time.time()
            attribute['total_time'] += attribute['end'] - attribute['start']
            self.update(attribute=attribute, action='reset_markers')

        elif action == 'reset_markers':
            attribute['start'] = float()
            attribute['end'] = float()

        elif action == 'reset':
            attribute['total_time'] = float()
            self.update(attribute=attribute, action='reset_markers')

    def approximate_simulation(self, iterations=int(), space=None):
        approximation = space.number_of_particles * iterations * self.approximation_constant
        return approximation

    @staticmethod
    def load(saved_timer):
        loaded_timer = Timer()
        loaded_timer.simulation['total_time'] = saved_timer['simulation']['total_time']
        loaded_timer.processing['total_time'] = saved_timer['processing']['total_time']
        return loaded_timer

    def dictionary(self):
        if self.running:
            self.stop()
            self.start()
        timer_dict = {'simulation': self.simulation, 'processing': self.processing}
        return timer_dict


if __name__ == '__main__':

    pass
