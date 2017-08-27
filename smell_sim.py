''' smell_sim.py
Manages running the simulation. Creates and displays the window,
updates the entities in the environment, and renders the entities within the environment.
'''
import sys
from hyperopt import hp
from hyperopt import fmin, tpe, STATUS_OK
from sympy.geometry import point

from world import SmellWorld
from world.view import WorldView
from entity.animond import SmellAnimond, AnimondView
from entity.home import Home, HomeView
from entity.food import Food, FoodView
from predictor import QPredictor

# Window information
WIDTH = 1000
HEIGHT = 800
DELAY = 0

NAME = 'Animonds'

GOAL_THRESHOLD = 20
RENDER = False

# Search space
EPISODES = 'episodes'
STEPS = 'steps'
REPLAY_SIZE = 'replay_size'
RANDOM_PERCENT = 'random_percent'
LEARNING_RATE = 'learning_rate'
DISCOUNT = 'discount'
MOMENTUM = 'momentum'
DROPOUT = 'dropout'


def create_search_space():
    return {
        EPISODES: hp.quniform(EPISODES, 1000, 10000, 1),
        STEPS: hp.quniform(STEPS, 500, 1000, 1),
        REPLAY_SIZE: hp.quniform(REPLAY_SIZE, 2, 30, 1),
        RANDOM_PERCENT: hp.uniform(RANDOM_PERCENT, 0.01, 0.5),
        LEARNING_RATE: hp.uniform(LEARNING_RATE, 0.00000001, 0.0001),
        DISCOUNT: hp.uniform(DISCOUNT, 0.9, 1.0),
        MOMENTUM: hp.uniform(MOMENTUM, 0.5, 0.75),
        DROPOUT: hp.uniform(DROPOUT, 0.25, 0.75)
    }


def optimize(args):

    print('Arguments: {}'.format(args))
    score = run(int(args[EPISODES]), int(args[STEPS]), int(args[REPLAY_SIZE]), args[RANDOM_PERCENT],
                args[LEARNING_RATE], args[DISCOUNT], args[MOMENTUM], args[DROPOUT])
    print(score)
    print('****************************')
    return {
        'status': STATUS_OK,
        'loss': sys.float_info.max - score,
        'attachments': {
            'args': args
        }
    }


def run(episodes,
        epochs,
        replay_size,
        random_percent,
        learning_rate,
        discount,
        momentum,
        dropout):
    predictor = QPredictor(epoch_size=epochs, replay_size=replay_size,
                           random_percent=random_percent, learning_rate=learning_rate,
                           discount=discount, momentum=momentum, dropout=dropout)
    animond = SmellAnimond('smell_animond', predictor, size=40, position=(400, 400))
    home = Home('home', position=point.Point2D(200, 700), color=(0, 0.1, 0.9), size=20)
    food = Food('food', position=point.Point2D(700, 100), color=(0, 1, 0), size=10)

    world_view = WorldView() if RENDER else None
    world = SmellWorld([animond], [home], [food], size=(WIDTH, HEIGHT), view=world_view, render=RENDER)

    animond.world = world
    animond.predictor.initialize(animond.state)

    if RENDER:
        animond.view = AnimondView()
        home.view = HomeView()
        food.view = FoodView()

    for i in range(episodes):
        sys.stdout.write('\rEpisode {}: {}'.format(i, world.run(epochs, train=True)))
        sys.stdout.flush()
        world.reset()

    return world.run(1, train=False)


def main():
    best = fmin(optimize,
                space=create_search_space(),
                algo=tpe.suggest,
                max_evals=100)

    print(best)


if __name__ == '__main__':
    main()
