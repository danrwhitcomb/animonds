from world import World
from util.geometry import distance


class AnimondWorld(World):

    def __init__(self,
                 animonds,
                 homes,
                 foods,
                 size=(800, 800),
                 view=None,
                 render=False,
                 goal_threshold=20):

        super().__init__(size, view, render)
        self.animonds = animonds
        self.homes = homes
        self.foods = foods
        self.goal_threshold = goal_threshold

    @property
    def entities(self):
        return self.animonds + self.homes + self.foods

    def run(self, steps, train):
        total = 0
        for _ in range(steps):
            total += sum([animond.tick(train) for animond in self.animonds])

            if self.render:
                self.view.tick(self.entities)

        return total

    def within_home_threshold(self, position):
        return self.within_entity_threshold(position, self.homes)

    def within_food_threshold(self, position):
        return self.within_entity_threshold(position, self.foods)

    def within_entity_threshold(self, position, entities):
        distances = self._get_distances_from_entities(position, entities)
        within_threshold = [d for d in distances if d < self.goal_threshold]
        return len(within_threshold) > 0

    def _get_distances_from_entities(self, position, entities):
        return [distance(position, entity.position) for entity in entities]

    def get_avg_distance_from_food(self, position):
        return self.get_avg_distance_from_entities(position, self.foods)

    def get_avg_distance_from_home(self, position):
        return self.get_avg_distance_from_entities(position, self.homes)

    def get_avg_distance_from_entities(self, position, entities):
        return sum(self._get_distances_from_entities(position, entities)) / len(entities)

    def save(self):
        for a in self.animonds:
            a.predictor.save()
