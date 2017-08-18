from entity import Entity


class Food(Entity):

    def __init__(self,
                 entity_id,
                 position,
                 view=None):
        super().__init__(entity_id, position)
        self.view = view

    def render(self):
        if self.view is not None:
            self.view.render(self.position)
