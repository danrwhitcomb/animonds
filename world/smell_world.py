from world import AnimondWorld


class SmellWorld(AnimondWorld):

    def __init__(self,
                 animonds,
                 homes,
                 foods,
                 size=(800, 800),
                 view=None,
                 render=False,
                 goal_threshold=20):
        super().__init__(animonds, homes, foods, size, view, render, goal_threshold)

    def get_reward(self, animond):
        distance = self.get_avg_distance_from_home(animond.position) if animond.has_food \
                else self.get_avg_distance_from_food(animond.position)
        
        return (1 / distance ** 2)
