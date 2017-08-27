
class World:

    def __init__(self,
                 size=(800, 800),
                 view=None,
                 render=False):
        self.view = view
        if view is not None:
            view.add_observer(self)

        self._entities = []
        self.size = size
        self.render = render

    @property
    def entities(self):
        return self._entities

    def __repr__(self):
        return 'World=entities={entities}, size={size}, render={render}'.format(entities=self.entities,
                                                                                size=self.size, render=self.render)

    def run(self, steps, train):
        raise NotImplementedError('run() has not been implemented!')

    def reset(self):
        for entity in self.entities:
            entity.reset()

    def get_reward(self, entity):
        raise NotImplementedError('get_reward() has not been implemented!')

    def transform_shape_for_bounds(self, shape):
        new_shape = shape
        for vertex in shape.vertices:
            if vertex.x > self.size[0]:
                new_shape = new_shape.translate(self.size[0] - vertex.x, 0)
            elif vertex.x < 0:
                new_shape = new_shape.translate(0 - vertex.x, 0)

            if vertex.y > self.size[1]:
                new_shape = new_shape.translate(0, self.size[1] - vertex.y)
            elif vertex.y < 0:
                new_shape = new_shape.translate(0, 0 - vertex.y)

        return new_shape

    def close(self):
        print('Closing world...')
        exit(0)

    def save(self):
        pass
