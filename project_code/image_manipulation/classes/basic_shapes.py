from project_code.my_maths import trigonometry as trig


class Circle:
    """
    A circle shape.

    The shape can generate would be indexes. It can be cast to a canvas by index.
    """
    def __init__(self, circle_radius, center_x, center_y):
        """
        Creates a Circle Object.

        The Circle object stores the attributes circle radius and circle center (x, y).
        It can be drawn, which calculates which indexes fall within the circle.

        Parameters
        ----------
        circle_radius: int
            Radius of the circle in amount of pixels.
        center_x: int
            X coordinate of the center of the pixel.
        center_y: int
            Y coordinate of the center of the pixel.

        Returns
        -------
        Circle
            The created Circle object.
        """
        self.radius = circle_radius
        self.center = (center_x, center_y)

    def circumference_indexes(self):
        """
        Computes which indexes fall on the circumference of the circle.

        Deletes all double indexes.

        Returns
        list: [(int, int)]
            Indexes of the circumference.
        """
        indexes = list()
        for degree in range(3600):
            degree //= 10

            x_shift, y_shift = trig.new_xy_circumference_circle(degree, self.radius)
            x_shift = int(x_shift)
            y_shift = int(y_shift)
            center_x, center_y = self.center
            xy = (center_x + x_shift, center_y + y_shift)

            if xy not in indexes:
                indexes.append(xy)

        return indexes

    def circumference_indexes_fitted(self, max_x, max_y, min_x, min_y):
        """
        Computes which indexes fall on the circumference of the circle within the canvas.

        Deletes all indexes that fall outside the bounds of the canvas and double indexes.

        Parameters
        ----------
        max_x: int
            Width of the canvas
        max_y: int
            Height of the canvas

        Returns
        -------
        list: [(int, int)]
            Indexes of the circumference within the bounds of the canvas.
        """
        potential_indexes = self.circumference_indexes()
        return partial_circle_circumference(potential_indexes, max_x, max_y, min_x, min_y)


def partial_circle_circumference(circle_indexes, max_x, max_y, min_x, min_y):
    """
    Casts a circle to a smaller canvas.

    Cuts off all indexes that don't fit on the new index.

    Parameters
    ----------
    circle_indexes: list [(int, int)]
        Indexes that belong to the circumference of the circle.
    max_x: int
        Maximum valid x index
    max_y: int
        Maximum valid y index.
    min_x: int
        Minimum valid x index.
    min_y: int
        Minimum valid y index.

    Returns
    -------
    list: [(int, int)]
        Valid indexes that belong to the circumference of the circle.
    """
    fitted_indexes = list()

    for x, y in circle_indexes:
        if x >= max_x or x <= min_x:
            continue
        if y >= max_y or y <= min_y:
            continue
        fitted_indexes.append((x, y))

    return fitted_indexes
