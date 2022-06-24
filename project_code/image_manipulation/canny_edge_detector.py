from project_code.my_maths import \
    select_from_matrix as select, \
    calculus as calculus

import numpy as np


def non_maximum_suppressor(image_pixel_table, kernel_size=5):
    """Turns of pixels in an image that are not the local maximum in the intersection of the edge."""
    print("Non maximum suppression.")

    image_values = image_pixel_table.pixels
    height, width = image_values.shape
    kernel_radius = kernel_size // 2
    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):
            current_pixel = image_values[row_index][column_index]
            if current_pixel.is_off():
                continue

            pixel_and_surrounding = select.get_sub_matrix(image_values,
                                                          row_index - kernel_radius,
                                                          column_index - kernel_radius,
                                                          size=kernel_size)

            intersection_edge = select.get_perpendicular_vector(pixel_and_surrounding,
                                                                current_pixel.orientation,
                                                                kernel_radius)
            # Calculates the local maximum of the intersection of the edge.
            local_maximum_index = calculus.local_maximum_vector(intersection_edge)
            # Turns off all pixels that aren't the local maximum in the edge.
            for edge_index, edge_pixel in enumerate(intersection_edge):
                if edge_index == local_maximum_index:
                    continue
                edge_pixel.turn_off()


def hysteresis_thresholding(image_pixel_table, kernel_size=5):
    """
    Turns off pixels below a certain threshold a, and keeps pixels on above threshold b.
    Pixels between the two thresholds are only kept on if they are connected (directly or indirectly) with a pixel that
    passes threshold b.
    """
    print('Hysteresis')
    kernel_radius = kernel_size // 2
    image_values = image_pixel_table.pixels
    height, width = image_values.shape
    brightness_scale = sorted(image_pixel_table.get_luminosity_active_pixels())

    high_threshold = np.percentile(brightness_scale, 70)
    low_threshold = high_threshold * 0.35

    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):

            if image_values[row_index][column_index] < low_threshold:
                image_values[row_index][column_index].turn_off()

    continuous_edges = image_pixel_table.find_continuous_edges()
    for edge in continuous_edges:
        edge.validate(high_threshold)


def canny_detector(image_pixel_table, kernel_size=5):
    non_maximum_suppressor(image_pixel_table, kernel_size)
    hysteresis_thresholding(image_pixel_table, kernel_size)

    return image_pixel_table
