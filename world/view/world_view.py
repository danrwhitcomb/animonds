import pyglet


class WorldView(pyglet.window.Window):

    def __init__(self, size=(800, 600)):
        super().__init__()
        self.observers = []
        self.set_size(size[0], size[1])

    def tick(self, entities):
        pyglet.clock.tick()

        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            self.draw_entities(entities)
            window.flip()

    def on_draw(self):
        self.clear()

    def draw_entities(self, entities):
        for entity in entities:
            entity.render()

    def add_observer(self, observer):
        self.observers.append(observer)

    def close(self):
        for ob in self.observers:
            ob.close()

    def save(self):
        for ob in self.observers:
            ob.save()

    def on_key_press(self, symbol: int, modifiers):
        if symbol == pyglet.window.key.Q:
            print("Exiting...")
            self.close()

        elif symbol == pyglet.window.key.S:
            print("Saving...")
            self.save()

    def on_window_close(self):
        self.event_loop.exit()
        return pyglet.event.EVENT_HANDLED
