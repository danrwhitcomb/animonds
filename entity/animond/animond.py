from math import pi
from sympy.geometry import polygon

from entity import Entity
from world import AnimondWorld

from util import geometry
from util.moves import FORWARD, LEFT_ROTATE, RIGHT_ROTATE

MOVE_DIST = 25
ROTATE_DIST = pi / 4.0


class Animond(Entity):

    def __init__(self,
                 entity_id,
                 predictor,
                 size,
                 color=(0, 0, 0),
                 view=None,
                 position=(0, 0),
                 angle=0,
                 has_food=False):
        super().__init__(entity_id, color)

        self.predictor = predictor
        self.angle = angle
        self.view = view
        self.has_food = has_food

        # Persist starting vals for reset
        self.start_angle = angle
        self.start_position = position
        self.start_has_food = self.has_food
        self.size = size

        self.create_shape(position, size, angle)

    def create_shape(self, position, size, angle):
        self.shape = polygon.Triangle(*geometry.get_iso_triangle_for_center(
                position, size, angle, 0.2))

    def reset(self):
        super().reset()
        self.angle = self.start_angle
        self.has_food = self.start_has_food
        self.predictor.reset(self.state)

        self.create_shape(self.start_position, self.size, self.angle)


    def render(self):
        if self.view is not None:
            self.view.render(self.shape, self.has_food)

    @property
    def position(self):
        return self.shape.circumcenter

    @property
    def state(self):
        raise NotImplementedError('get_state() has not been implemented!')

    @state.setter
    def state(self, value):
        pass

    def collision(self, source, angle):
        return self.shape.intersection(line.Ray(source, angle))

    def run(self, steps, train=False):
        return (sum([self.tick(train) for _ in range(steps)]) / steps)

    def tick(self, train=False):
        had_food = self.has_food
        move = self.predictor.get_move()

        # Get the original move
        first_state = self.state

        # Apply the move to the model, thus moving the animond
        self.update_state(move)

        # Get the resulting animond state and the reward
        second_state = self.state

        # If the update caused a food exchange, the move gets
        # additional reward
        food_score = 1 if had_food ^ self.has_food else 0
        reward = self.world.get_reward(self) + food_score

        # Update the predictor with the new transition
        if train:
            self.predictor.update(move, reward, first_state, second_state)

        return reward

    def update_state(self, move):
        self._apply_move(move)

        if isinstance(self.world, AnimondWorld):
            if self.has_food and self.world.within_home_threshold(self.position):
                self.has_food = False
            elif not self.has_food and self.world.within_food_threshold(self.position):
                self.has_food = True

    def _apply_move(self, move):
        self.lock = True

        if move == FORWARD:
            translation = geometry.get_point_in_direction(self.position, self.angle, MOVE_DIST) - self.position
            self.shape = self.shape.translate(*translation)
            self.shape = self.world.transform_shape_for_bounds(self.shape)
        elif move == LEFT_ROTATE:
            self.angle -= ROTATE_DIST
            self.shape = self.shape.rotate(ROTATE_DIST, self.position)
        elif move == RIGHT_ROTATE:
            self.angle += ROTATE_DIST
            self.shape = self.shape.rotate(-ROTATE_DIST, self.position)
        else:
            print("Move not found")

        self.lock = False
