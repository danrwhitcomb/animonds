from math import sqrt

from entity.animond import Animond
from world import AnimondWorld
from util import geometry
import error


class SmellAnimond(Animond):

    def __init__(self,
                 entity_id,
                 predictor,
                 view,
                 position=(0, 0),
                 angle=0,
                 has_food=False):
        super().__init__(entity_id, predictor, view, position, angle, has_food)

    @property
    def state(self):
        world_size = self.world.size
        normalized_position = geometry.normalize_position(self.position, world_size)
        normalized_angle = geometry.normalize_angle(self.angle)
        state = (normalized_position[0], normalized_position[1], normalized_angle)

        if (self.world is not None and isinstance(self.world, AnimondWorld)):
            distance_from_goal = self.world.get_avg_distance_from_home(self.position) \
                                        if self.has_food else self.world.get_avg_distance_from_food(self.position)
            state += (distance_from_goal / (sqrt((world_size[0] ** 2) + (world_size[1] ** 2))),)
        else:
            raise error.IncompatibleEntityError('The world used is not a sub-class of AnimondWorld')

        return state

    @state.setter
    def state(self, state):
        self.position = state['location']
        self.angle = state['angle']
        self.has_food = state['has_food']
