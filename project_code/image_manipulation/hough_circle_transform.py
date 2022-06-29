from project_code.image_manipulation.classes import basic_shapes as shapes

from project_code.my_maths import \
    calculus as calc, \
    select_from_matrix as matrix_select

import numpy as np


def draw_around_pixels(value_table, circle_indexes, radius):
    """
    Draws a circle in around every pixel.

    The circles are drawn in cache space by adding 1 to the cache. All circles have the same radius.

    Parameters
    ----------
    value_table: pix.PixelTable
        The table matrix containing all the values of the edges. The objects inside pixel table have to have a cache
        attribute the function can use.
    circle_indexes: list [(int, int)]
        Minimum value to be considered a peak.
    radius: int
        Radius of the circle.

    Returns
    -------
    Nothing
        The circles have been drawn in cache space.
    """
    accumulator = 1 / len(circle_indexes)
    image_values = value_table.pixels
    height, width = image_values.shape

    right_border_start = width - radius
    lower_border_start = height - radius

    for row_index in range(radius, height - radius):
        cast_circle = circle_indexes.copy()

        # Casts the circle if it doesn't fit in the y direction to fit on the canvas.
        if row_index < radius:
            cast_circle = shapes.partial_circle_circumference(cast_circle,
                                                              row_index,
                                                              radius,
                                                              -radius,
                                                              -radius)
        elif row_index > lower_border_start:
            cast_circle = shapes.partial_circle_circumference(cast_circle,
                                                              radius,
                                                              radius,
                                                              row_index - height,
                                                              -radius)

        for column_index in range(radius, width - radius):
            current_pixel = image_values[row_index][column_index]
            if current_pixel.is_off():
                continue

            # Casts the circle (further) if the circle does not fit in the x direction.
            if column_index < radius:
                cast_circle = shapes.partial_circle_circumference(cast_circle.copy(),
                                                                  radius,
                                                                  column_index,
                                                                  -radius,
                                                                  -radius)
            elif column_index > right_border_start:
                cast_circle = shapes.partial_circle_circumference(cast_circle.copy(),
                                                                  radius,
                                                                  radius,
                                                                  -radius,
                                                                  column_index - width)

            for x_shift, y_shift in cast_circle:
                perimeter_pixel = image_values[row_index + y_shift][column_index + x_shift]
                if perimeter_pixel.cache is None:
                    perimeter_pixel.cache = accumulator
                else:
                    perimeter_pixel.cache += accumulator


def find_accumulator_peaks(value_table, threshold, radius):
    """
    Finds peaks inside the cache of the pixel.

    Parameters
    ----------
    value_table: pix.PixelTable
        The table matrix containing all the values of the edges. The objects inside pixel table have to have a cache
        attribute the function can use.
    threshold: float
        Minimum value to be considered a peak.
    radius: int
        Radius of the circle we are looking for.

    Returns
    -------
    list: [(int, int)]
        location of the found peaks as (x, y)
    """
    found_peaks = []
    image_values = value_table.pixels
    height, width = image_values.shape

    for row_index in range(radius, height - radius):
        for column_index in range(radius, width - radius):
            current_pixel = image_values[row_index][column_index]
            if current_pixel.cache is None:
                continue
            if current_pixel.cache > threshold:
                # Saves the circle center as (x, y, magnitude).
                local_neighborhood = matrix_select.get_sub_matrix(mother_matrix=image_values,
                                                                  x_start=row_index,
                                                                  y_start=column_index,
                                                                  size=radius)

                maximum_index, local_maximum = calc.local_maximum_2d_cache(local_neighborhood)
                local_maximum_x, local_maximum_y = maximum_index
                found_peaks.append((column_index + local_maximum_x, row_index + local_maximum_y, local_maximum))

    return found_peaks


def find_circles_set_radius(value_table, radius):
    """
    Searches an image for circles.

    Searches an image inside a Pixel Table for circles using the hough circle transform.
    Draws a circle around point 0 and saves the indexes.
    Draws a circle around every pixel that is turned on. All pixels that get drawn on get a count.
    The pixels with a count higher than amount on indexes inside the circle * 0.5 are considered candidates for a
    circle.

    Parameters
    ----------
    value_table: pix.PixelTable
        The table matrix containing all the values of the edges. The objects inside pixel table have to have a cache
        attribute the function can use.
    radius: int
        Radius of the circle we are looking for.

    Returns
    -------
    list: [(int, int)]
        Centers of all found circles as (x, y)
    """
    print('Hough {}'.format(radius))

    base_circle = shapes.Circle(radius, 0, 0)
    base_circle_indexes = base_circle.circumference_indexes()

    draw_around_pixels(value_table, base_circle_indexes, radius)

    threshold = 0.5
    found_circle_centers = find_accumulator_peaks(value_table, threshold, radius)

    value_table.clear_cache()

    return found_circle_centers


def find_circles_unset_size(value_table, size=2):
    """
    Searches the image inside the pixel table for circles.

    Searches for a specified range of radii.

    Parameters
    ----------
    value_table: pix.PixelTable
        The table matrix containing all the values of the edges. The objects inside pixel table have to have a cache
        attribute the function can use.
    size: int
        Signifies the range of radii to look for.

    Returns
    -------
    dict: {int: [(int, int)]}
        Radii with a list containing the centers of the found circles of that radius.
    """
    radius_range = {0: range(10, 201),
                    1: range(6, 15),
                    2: range(15, 31),
                    3: range(30, 101),
                    4: range(60, 101),
                    5: range(100, 201)}

    potential_circle_centers = dict()
    for radius in radius_range[size]:
        potential_circle_centers[radius] = find_circles_set_radius(value_table, radius)

    """
    Search for the maximum in nearby 3d space. 

    The first two dimensions are the x and y axis in the image (width and height). The last dimension is the radius 
    size.
    Searches for a higher peak near the given circle center.
    """
    circle_centers = dict()

    wanted_count = len(potential_circle_centers)
    count = 0
    while count != wanted_count:
        count = 0
        for radius in potential_circle_centers:
            if len(potential_circle_centers[radius]) == 0:
                count += 1
                continue
            if radius not in circle_centers:
                circle_centers[radius] = list()

            x_coordinate, y_coordinate, magnitude = potential_circle_centers[radius][0]
            radius_3d_space = radius // 2
            magnitude_3d_space = constructs_magnitudes_in_3d_space(potential_circle_centers,
                                                                   x_coordinate,
                                                                   y_coordinate,
                                                                   radius,
                                                                   radius_3d_space,
                                                                   delete=True)

            magnitude_index, biggest_magnitude = calc.local_maximum_3d(magnitude_3d_space)
            magnitude_index = (magnitude_index[0] + x_coordinate - radius_3d_space,
                               magnitude_index[1] + y_coordinate - radius_3d_space)

            circle_centers[radius].append(magnitude_index)

    return circle_centers


def constructs_magnitudes_in_3d_space(data_dict, x_start, y_start, z_start, radius=10, delete=False):
    """
    Constructs a 3d matrix.

    The 3d matrix is filled with the pixels cache of every pixel inside the bounds of the parameters.
    Z is the key in the dictionary. All values will be searched with a range of radius in both positive and negative
    direction. All values that can't be found will be assigned 0.

    Parameters
    ----------
    data_dict: dict {int: [(int, int)]}
        Dictionary containing point in the 3d space.
    x_start: int
        x coordinate of the center.
    y_start: int
        y coordinate of the center.
    z_start: int
        z coordinate of the center.
    radius: int
        Radius of the 3d space to construct around the center.
    delete: bool
        Deletes all values put into the 3d space from ``data_dict``.

    Returns
    -------
    numpy.ndarray
        The constructed 3d space.
    """
    magnitude_3d_space = np.zeros((radius * 2, radius * 2, radius * 2))

    for height_index in range(radius * 2):
        try:
            circle_centers = data_dict[z_start + height_index - radius]
        except KeyError:
            continue

        # searches for peaks that are located nearby.
        nearby_peaks = [(x, y, magnitude) for x, y, magnitude in circle_centers
                        if x_start - radius <= x < x_start + radius
                        and y_start - radius <= y < y_start + radius]
        for x, y, magnitude in nearby_peaks:
            magnitude_3d_space[height_index][y + radius - y_start][x + radius - x_start] = magnitude
            if delete:
                list_with_centers = data_dict[z_start + height_index - radius]
                list_with_centers.remove((x, y, magnitude))

    return magnitude_3d_space
