import math


def calculate_hypotenuse(side_1, side_2):
    """
    Calculates the length of the hypotenuse of a triangle using Pythagoras theorem.

    This function calculates the length of the hypotenuse of a triangle with a 90-degree angle, by using the length of
    the other two sides of the triangle and pythagoras theorem.

    Parameters
    ----------
    side_1 : int
        Length of a leg of the triangle
    side_2 : int
        Length of the other leg of the triangle

    Returns
    -------
    int
        Length of the hypotenuse.
    """
    return math.sqrt(side_1 ** 2 + side_2 ** 2)


def approximate_hypotenuse(side_1, side_2):
    """
    Calculates the approximate length of the hypotenuse.

    Sums the absolute values of the two sides of the triangle to approximate the length of the hypotenuse.

    Parameters
    ----------
    side_1: float
        Length of one side of the 90° triangle
    side_2: float
        Length of another side of the 90° triangle

    Returns
    -------
    float
        Approximate length of the hypotenuse.
    """
    return abs(side_1) + abs(side_2)


def calculate_gradient_angle(x_response, y_response):
    """
    Calculates the gradient orientation (of a pixel) based on their x and y response to the sobel kernel.

    Parameters
    ----------
    x_response: float
        Response to the vertical sobel kernel.
    y_response: float
        Response of the horizontal sobel kernel.

    Returns
    -------
    float
        The orientation of the pixel in degrees.
    """
    if x_response == 0:
        return 1
    return math.atan(y_response / x_response)


def new_xy_circumference_circle(angle, radius):
    """
    Calculates the x and y coordinates on the circumference of a circle.

    The coordinates are calculated with the angle and radius and are indexed with respect to their shift from the circle
    center.

    Parameters
    ----------
    angle: float
        Angle from the x-axis in degrees.
    radius: int
        Radius of the circle.

    Returns
    -------
    tuple : (int, int)
        The new x, y coordinates.
    """
    return math.cos(radius * angle), math.sin(radius * angle)
