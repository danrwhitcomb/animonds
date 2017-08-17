

class Entity(object):

    def __init__(self,
                 entity_id,
                 position):
        self.id = entity_id
        self.lock = False

        self.world = None
        self.position = position
        self.start_position = position

    def reset(self):
        self.position = self.start_position

    def tick(self, train=False):
        pass

    def render(self):
        pass

    @property
    def state(self):
        pass
