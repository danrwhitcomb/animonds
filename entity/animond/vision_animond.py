
from entity import animond
from world import VisionWorld

class VisionAnimond(animond.Animond):

    def __init__(self,
                 entity_id,
                 predictor,
                 size,
                 fov,
                 color=(0, 0, 0),
                 view=None,
                 position=(0, 0),
                 angle=0,
                 has_food=False):
        super().__init__(entity_id, predictor, size, color, view, position, angle, has_food)
        self.fov = fov

    @property
    def state(self):
        if (self.world is not None and isinstance(self.world, VisionWorld)):
            return self.world.get_view(self.position, self.angle, self.fov, 32)

        return []
        
    @state.setter
    def state(self, state):
        self.position = state['location']
        self.angle = state['angle']
        self.has_food = state['has_food']
