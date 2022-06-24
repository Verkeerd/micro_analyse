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
    int : Length of the hypotenuse.
    """
    return math.sqrt(side_1 ** 2 + side_2 ** 2)


def approximate_hypotenuse(side_1, side_2):
    return abs(side_1) + abs(side_2)


def round_angle(angle):
    """
    Rounds an angle.

    This function rounds an angle to the closest of four angles:
    The vertical-, horizontal- or one of the two diagonal directions.

    Parameters
    ----------
    angle: float
        The angle.

    Returns
    -------
    int
        The rounded angle.
    """
    if angle <= -0.225:
        return round_angle(angle + 3.6)
    if angle <= 0.225:
        return 0
    if angle <= 0.675:
        return 45
    if angle <= 1.125:
        return 90
    if angle <= 1.575:
        return 135
    if angle <= 2.025:
        return 180
    if angle <= 2.475:
        return 225
    if angle <= 2.925:
        return 270
    if angle <= 3.375:
        return 315
    return round_angle(angle - 3.6)


def perpendicular_to_rounded_angle(angle):
    """
    Gets the angle curring perpendicular to the current angle.


    Parameters
    -----------
    angle : float
         The angle perpendicular to a random side of the current angle.
    :return:
    """
    angle += 90
    if angle > 360:
        angle -= 360
    return angle


def calculate_angle_sobel(x_response, y_response):
    if y_response == 0:
        return 90
    return math.atan(x_response / y_response)


def new_xy_circumferance_circle(angle, radius):
    """"""
    return radius * math.cos(angle), radius * math.sin(angle)