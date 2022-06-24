import my_maths.trigonometry as trig


class Circle:
    """"""
    def __init__(self, circle_radius, center_x, center_y):
        self.radius = circle_radius
        self.center = (center_x, center_y)

    def draw(self):
        indexes = list()
        for degree in range(3600):
            degree //= 10

            x_shift, y_shift = trig.new_xy_circumferance_circle(degree, self.radius)
            x_shift = int(x_shift)
            y_shift = int(y_shift)
            center_x, center_y = self.center
            xy = (center_x + x_shift, center_y + y_shift)

            if xy not in indexes:
                indexes.append(xy)

        return indexes
