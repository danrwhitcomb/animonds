from sympy.geometry import ellipse
from entity import Entity


class Food(Entity):

    def __init__(self,
                 entity_id,
                 position,
                 size,
                 color,
                 view=None):
        super().__init__(entity_id, color)
        self.view = view
        self.shape = ellipse.Circle(position, size)

    def render(self):
        if self.view is not None:
            self.view.render(self.position, self.shape.radius, self.color)

    @property
    def position(self):
        return self.shape.center

    def collision(self, source, angle):
        return self.shape.intersection(line.Ray(source, angle))
