import sys

import world


class VisionWorld(world.AnimondWorld):
    ''' A world which can be viewed by entities
        in two dimensions.

        It is capable of returning a view based on some point and direction
    '''
    
    def get_view(self, position, angle, fov, resolution):
        view = []
        angle_diff = fov / 2
        for i, direction in enumerate(range(angle - angle_diff, angle + angle_diff, resolution)):
            min_dist = sys.float_info.max
            min_color = None
            for entity in self.entities:
                dist, color = entity.collision(position, direction)
                if dist is not None and min_dist > dist:
                    min_dist = dist
                    min_color = color

            view[i] = min_color

        return view
