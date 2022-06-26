from project_code.my_maths import \
    select_from_matrix as select, \
    calculus as calculus

import numpy as np


def non_maximum_suppressor(image_pixel_table, kernel_size=5):
    """
    Turns off all pixels that have not been marked as local maximum.

    Checks for the pixel that is turned on if they are a local maximum. This local maximum is checked on the
    intersection of the edge, in order to thin it.

    Parameters
    ----------
    image_pixel_table: PixelTable
        Pixel table containing Grey Pixels.
    kernel_size: int
        Diameter of the to evaluate edge intersection.

    Returns
    -------
    None
        All pixels in the intersection that aren't the local maximum have been turned off.
    """
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

            intersection_edge = select.get_vector_on_angle(pixel_and_surrounding,
                                                           current_pixel.orientation,
                                                           kernel_radius)
            # Calculates the local maximum of the intersection of the edge.
            local_maximum_index = calculus.local_maximum_1d(intersection_edge)
            # Turns off all pixels that aren't the local maximum in the edge.
            for edge_index, edge_pixel in enumerate(intersection_edge):
                if edge_index == local_maximum_index:
                    continue
                edge_pixel.turn_off()


def hysteresis_thresholding(image_pixel_table, kernel_radius=5):
    """
    Turns off weak edges based on hysteresis thresholding.

    The high hysteresis threshold is the value of the 80th percentile of pixel values.
    The low hysteresis threshold is 35% of the high threshold.

    Turns off pixels below a certain threshold a, and keeps pixels on above threshold b.
    Pixels between the two thresholds are only kept on if they are connected (directly or indirectly) with a pixel that
    passes threshold b.

    Parameters
    ----------
    image_pixel_table: PixelTable
        The pixel table containing the greyscale variants of pixels of an image.
    kernel_radius: int
        The maximum distance between adjacent pixels with creating edges.

    Returns
    -------
    None
        All pixels that don't qualify for hysteresis thresholding have been turned off.
    """
    print('Hysteresis')
    image_values = image_pixel_table.pixels
    height, width = image_values.shape
    brightness_scale = sorted(image_pixel_table.get_luminosity_active_pixels())

    high_threshold = np.percentile(brightness_scale, 90)
    low_threshold = high_threshold * 0.35

    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):

            if image_values[row_index][column_index] < low_threshold:
                image_values[row_index][column_index].turn_off()

    continuous_edges = image_pixel_table.find_continuous_edges()
    for edge in continuous_edges:
        edge.validate(high_threshold)


def canny_detector(image_pixel_table, kernel_size=5):
    """
    Apply the canny edge detector.

    Transforms a pixel table containing Grey Pixels by turning off all pixels that are not a local maximum and applying
    hysteresis thresholding.

    Parameters
    ----------
    image_pixel_table: PixelTable
        The Pixel Table contain Grey Pixels. Assumed to contain output from sobel edge detector.
    kernel_size: int
        Diameter of the non-maximum edge intersection; (Double the) length between adjacent pixels with creating edges
        with hysteresis thresholding.

    Returns
    -------
    None
        The Pixel Table's content has been deleted. The output of the canny edge detector has been stored inside the
        Pixel Table.
    """
    non_maximum_suppressor(image_pixel_table, kernel_size)
    hysteresis_thresholding(image_pixel_table, kernel_size // 2)
