import pyglet
from time import sleep

from models import Animond, Food, Home
from views import AnimondView, HomeView, FoodView
from predictor import RandomPredictor

WIDTH = 1000
HEIGHT = 800
DELAY = 0.5

NAME = 'Animonds'


class Env(pyglet.window.Window):

    def __init__(self, predictor, anim_ids, food_ids, home_ids):
        super(Env, self).__init__(WIDTH, HEIGHT)

        self.predictor = predictor

        self.anims = {i: Animond(i, (500, 400)) for i in anim_ids}
        self.homes = {i: Home(i) for i in food_ids}
        self.foods = {i: Food(i) for i in home_ids}

        self.anim_views = {anim: AnimondView(anim) for anim in self.anims.values()}
        self.home_views = {home: HomeView(home) for home in self.homes.values()}
        self.food_views = {food: FoodView(food) for food in self.foods.values()}

    def update(self, dt):
        pass

    def run(self):
        while True:
            pyglet.clock.tick()

            for window in pyglet.app.windows:
                for id, anim in self.anims.items():
                    move = self.predictor.getMove(anim)
                    anim.applyMove(move)

                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()

            sleep(DELAY)

    def on_draw(self):
        self.clear()
        for id, animond_view in self.anim_views.items():
            animond_view.render()

    def on_window_close(self):
        self.event_loop.exit()
        return pyglet.event.EVENT_HANDLED


if __name__ == '__main__':
    predictor = RandomPredictor()
    print("Starting...")
    env = Env(predictor, [2, 3], [1], [1])
    env.run()
