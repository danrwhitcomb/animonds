

class Predictor(object):

    def get_move(self):
        raise NotImplementedError('get_move() is not implemented!')

    def update(self, action, reward, start_state, end_state):
        raise NotImplementedError('update() is not implemented')

    def reset(self):
        raise NotImplementedError('reset() is not implemented')

    def save(self):
        pass

    def load(self):
        pass

    def close(self):
        pass
