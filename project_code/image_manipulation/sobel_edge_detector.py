from project_code.my_maths import \
    select_from_matrix as select, \
    trigonometry as trig


def sobel_calculation(matrix, kernel_radius=1, adjusted_size=2):
    """
    Calculates the result of a matrix and both sobel kernels.

    The sobel kernels are 3x3. The result of the kernel is normalised before being returned. The calculations are done
    separately without using matrices, so we don't compute the row with products with zero, which we already know does
    not influence the result.

    Parameters
    ----------
    matrix: numpy.ndarray
        Part of the image to apply the sobel kernel to.
    kernel_radius: int
        Radius of the kernel.
    adjusted_size: int
        Diameter of the kernel minus one.

    Returns
    -------
    tuple: (int, int)
        The horizontal weight.
        The vertical weight.
    """
    horizontal = 0
    vertical = 0
    normaliser = 0
    for i in range(kernel_radius):
        factor = i + 1
        normaliser += 2 * factor * (kernel_radius + 2)
        row_horizontal = matrix[i][kernel_radius] * factor * 2 - matrix[adjusted_size - i][kernel_radius] * factor * 2

        row_vertical = matrix[kernel_radius][adjusted_size - i] * factor * 2 - matrix[kernel_radius][i] * factor * 2

        for j in range(kernel_radius):
            row_horizontal += matrix[i][j] * factor\
                              + matrix[i][adjusted_size - j] * factor \
                              - matrix[adjusted_size - i][j] * factor \
                              - matrix[adjusted_size - i][2] * factor

            row_vertical += matrix[j][adjusted_size - i] * factor \
                            + matrix[kernel_radius - j][adjusted_size - i] * factor \
                            - matrix[j][i].value * factor \
                            - matrix[kernel_radius - j][i] * factor

        horizontal += row_horizontal
        vertical += row_vertical

    normaliser = 1 / normaliser

    return horizontal * normaliser, vertical * normaliser


def run_sobel_edge_detection(value_table, kernel_size=3):
    """
    Searches for edges inside the image in the pixel table.

    Searches for edges using the sobel operator. Calculates the magnitude and gradiant orientation for each found edge
    inside the image. Stores the results inside the pixel table.

    Parameters
    ----------
    value_table:
        Pixel Table containing the pixels to manipulate.
    kernel_size:
        Size of the sobel kernel.

    Returns
    -------
    None
        Pixels inside the Pixel Table contain the result of the sobel operator.
    """
    image_pixels = value_table.pixels
    height, width = image_pixels.shape
    kernel_radius = kernel_size // 2
    # Kernel_min_one is calculated here so it doesn't have to be computed for every element within the loop.
    kernel_min_one = kernel_size - 1
    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):
            local_neighborhood = select.get_sub_matrix(image_pixels,
                                                       row_index - kernel_radius,
                                                       column_index - kernel_radius,
                                                       size=kernel_size)

            horizontal_strength, vertical_strength = sobel_calculation(local_neighborhood,
                                                                       kernel_radius=kernel_radius,
                                                                       adjusted_size=kernel_min_one)

            total_strength = trig.approximate_hypotenuse(horizontal_strength, vertical_strength)
            image_pixels[row_index][column_index].cache = total_strength

            gradient_orientation = trig.calculate_gradient_angle(vertical_strength, horizontal_strength)
            image_pixels[row_index][column_index].orientation = gradient_orientation

    value_table.set_new_pixel_values()
