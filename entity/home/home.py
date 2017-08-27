from sympy.geometry import polygon
from sympy.geometry import line

from entity import Entity


class Home(Entity):

    def __init__(self,
                 entity_id,
                 position,
                 color,
                 size,
                 view=None):
        super().__init__(entity_id, color)
        self.view = view
        self.shape = polygon.RegularPolygon(position, size, 4)


    def render(self):
        if self.view is not None:
            self.view.render(self.shape.center, self.shape.radius, self.color)

    @property
    def position(self):
        return self.shape.center

    def collision(self, source, angle):
        return self.shape.intersection(line.Ray(source, angle))
