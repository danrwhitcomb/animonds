
class World(object):

    def __init__(self,
                 size=(800, 800),
                 view=None,
                 render=False) -> None:
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

    def transform_position_for_bounds(self, proposed_move):
        transformed_x: float = proposed_move[0]
        transformed_y: float = proposed_move[1]

        # constrain X coordinate
        transformed_x = 0 if transformed_x < 0 else transformed_x
        transformed_x = self.size[0] if transformed_x > self.size[0] else transformed_x

        # constrain y coordinate
        transformed_y = 0 if transformed_y < 0 else transformed_y
        transformed_y = self.size[1] if transformed_y > self.size[1] else transformed_y

        return (transformed_x, transformed_y)

    def close(self):
        print('Closing world...')
        exit(0)

    def save(self):
        pass
