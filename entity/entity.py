

class Entity:

    def __init__(self,
                 entity_id,
                 color):
        self.id = entity_id
        self.color = color

        self.lock = False
        self.world = None

    def tick(self, train=False):
        pass

    def render(self):
        pass

    @property
    def position(self):
        pass

    @property
    def state(self):
        pass

    def collision(self, source, angle):
        return None, None

    def reset(self):
        pass
