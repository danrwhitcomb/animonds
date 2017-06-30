''' env.py
Manages running the simulation. Creates and displays the window,
updates the entities in the environment, and renders the entities within the environment.
'''
import pyglet
from time import sleep
from math import pi, sqrt

from models import Animond, Food, Home
from views import AnimondView, HomeView, FoodView
from predictor import RandomPredictor, QPredictor
from estimator import deep_estimator
from util.geometry import distance, angle_difference

# Window information
WIDTH = 1000
HEIGHT = 800
DELAY = 0

NAME = 'Animonds'

GOAL_THRESHOLD = 5

# Shape that will be used as the input_dim
# of the estimator
#
# Current: (x, y, angle of rotation, has_food)
DATA_SHAPE = (4)

class Env(pyglet.window.Window):

    def __init__(self, predictors, anims, food, home):
        super(Env, self).__init__(WIDTH, HEIGHT)

        if len(predictors) != len(anims):
            raise ValueError('The number of predictors must match the number animonds')

        self.predictors = {i: predictor for i, predictor in enumerate(predictors)}

        self.anims = {i: anim for i, anim in enumerate(anims)}
        self.homes = {i: home for i, home in enumerate(food)}
        self.foods = {i: food for i, food in enumerate(home)}

        self.anim_views = {anim: AnimondView(anim) for anim in self.anims.values()}
        self.home_views = {home: HomeView(home) for home in self.homes.values()}
        self.food_views = {food: FoodView(food) for food in self.foods.values()}

        self.reset()

    def reset(self):
        for i, anim in self.anims.items():
            self.predictors[i].reset(self.get_animond_state(anim))

    def run(self, steps):
        for i in range(steps):
            pyglet.clock.tick()

            for window in pyglet.app.windows:
                for i, anim in self.anims.items():
                    predictor = self.predictors[i]
                    move = predictor.get_move()

                    # Get the original move
                    first_state = self.get_animond_state(anim)

                    # Apply the move to the model, thus moving the animond
                    self.update_animond_state(anim, move)

                    # Get the resulting animond state and the reward
                    second_state = self.get_animond_state(anim)
                    reward = self.get_animond_reward(anim)

                    # Update the predictor with the new transition
                    predictor.update(move, reward, first_state, second_state)

                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()

            sleep(DELAY)

    def get_animond_state(self, animond):
        norm_loc = normalize_location(animond.loc, (WIDTH, HEIGHT))
        distance = sum(self.get_distances_from_goals(animond)) / (sqrt((HEIGHT ** 2) + (WIDTH ** 2)))
        return norm_loc + (normalize_angle(animond.angle), distance, int(animond.has_food))

    def update_animond_state(self, animond, move):
        animond.apply_move(move)
        goals = self.homes.values() if animond.has_food else self.foods.values()

        distances = self.get_distances_from_goals(animond)
        within_threshold = [d for d in distances if d < GOAL_THRESHOLD]
        if len(within_threshold) > 1:
            animond.has_food = not animond.has_food

    def get_distances_from_goals(self, animond):
        goals = self.homes.values() if animond.has_food else self.foods.values()
        return [distance(animond.loc, goal.loc) for goal in goals]

    def get_animond_reward(self, animond):
        distances = self.get_distances_from_goals(animond)
        distance_reward = sum([1 / dist for dist in distances]) / len(distances)

        return distance_reward

    def get_animonds(self):
        return self.anims.values()

    def on_draw(self):
        self.clear()
        for animond_view in self.anim_views.values():
            animond_view.render()

        for home_view in self.home_views.values():
            home_view.render()

        for food_view in self.food_views.values():
            food_view.render()

    def on_window_close(self):
        self.event_loop.exit()
        return pyglet.event.EVENT_HANDLED

def normalize_location(location, max_vals):
    return (float(location[0]) / max_vals[0], float(location[1] / max_vals[1]))

'''
Normalizes an angle in radians
'''
def normalize_angle(angle):
    return angle / (2.0 * pi)

if __name__ == '__main__':
    time_steps = 100
    state_size = 5
    replay_size = 5
    print("Starting...")
    predictor = QPredictor(time_steps, state_size, replay_size)
    anim = Animond(1, (500, 400), (WIDTH, HEIGHT))
    food = Food(1, (200, 700))
    home = Home(1, (600, 100))

    env = Env([predictor], [anim], [home], [food])

    while True:
        env.run(time_steps)
        animonds = env.get_animonds()
        for anim in animonds:
            anim.set_state((500, 400), 0, 0)

        env.reset()
