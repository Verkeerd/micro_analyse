from project_code.my_maths import \
    select_from_matrix as select, \
    trigonometry as trig


def sobel_calculation(matrix):
    """
    Calculates the result of a matrix and both sobel kernels.

    The sobel kernels are 3x3. The result of the kernel is normalised before being returned.

    Parameters
    ----------
    matrix: numpy.ndarray
        Part of the image to apply the sobel kernel to.

    Returns
    -------
    int, int
        The horizontal weight.
        The vertical weight.
    """
    horizontal = matrix[0][0].value + 2 * matrix[0][1].value + matrix[0][2].value \
                 - matrix[2][0].value - 2 * matrix[2][1].value - matrix[2][2].value
    vertical = -matrix[0][0].value - 2 * matrix[1][0].value - matrix[2][0].value \
               + matrix[0][2].value + 2 * matrix[1][2].value + matrix[2][2].value
    return horizontal * 0.125, vertical * 0.125


def run_sobel_edge_detection(value_table):
    """
    Searches for edges inside the image in the pixel table.

    Searches for edges using the sobel operator. Calculates the magnitude and gradiant orientation for each found edge
    inside the image. Stores the results inside the pixel table.

    Parameters
    ----------
    value_table:
        Pixel Table containing the pixels to manipulate.

    Returns
    -------
    None
        Pixels inside the Pixel Table contain the result of the sobel operator.
    """
    kernel_size = 3
    image_pixels = value_table.pixels
    height, width = image_pixels.shape
    kernel_radius = 1
    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):
            pixel_and_surrounding = select.get_sub_matrix(image_pixels,
                                                          row_index - kernel_radius,
                                                          column_index - kernel_radius,
                                                          size=kernel_size)

            horizontal_strength, vertical_strength = sobel_calculation(pixel_and_surrounding)

            total_strength = trig.approximate_hypotenuse(horizontal_strength, vertical_strength)
            image_pixels[row_index][column_index].cache = total_strength

            gradient_orientation = trig.calculate_gradient_angle(vertical_strength, horizontal_strength)
            image_pixels[row_index][column_index].orientation = gradient_orientation

    value_table.set_new_pixel_values()
