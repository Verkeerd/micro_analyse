from project_code.image_manipulation.classes import basic_shapes as shapes


def find_circles_hough(value_table, radius):
    """
    Searches an image for circles.

    Searches an image inside a Pixel Table for circles using the hough circle transform.
    Draws a circle around point 0 and saves the indexes.
    Draws a circle around every pixel that is turned on. All pixels that get drawn on get a count.
    The pixels with a count that is higher than amount on indexes inside the circle * 0.5 are considered candidates for
    a circle.
    """
    print('Hough {}'.format(radius))

    base_circle = shapes.Circle(radius, 0, 0)
    base_circle_indexes = base_circle.draw()
    accumulator = 1

    image_values = value_table.pixels
    height, width = image_values.shape

    for row_index in range(radius, height - radius):
        for column_index in range(radius, width - radius):
            current_pixel = image_values[row_index][column_index]
            if current_pixel.is_off():
                continue
            for x_shift, y_shift in base_circle_indexes:
                perimeter_pixel = image_values[row_index + y_shift][column_index + x_shift]
                if perimeter_pixel.cache is None:
                    perimeter_pixel.cache = accumulator
                else:
                    perimeter_pixel.cache += accumulator

    found_circle_centers = list()
    threshold = 0.5 * len(base_circle_indexes)

    for row_index in range(radius, height - radius):
        for column_index in range(radius, width - radius):
            current_pixel = image_values[row_index][column_index]
            if current_pixel.cache is None:
                continue
            if current_pixel.cache > threshold:
                # Saves the circle center as (radius, x, y).
                found_circle_centers.append((radius, column_index, row_index))

    value_table.clear_cache()

    return found_circle_centers
