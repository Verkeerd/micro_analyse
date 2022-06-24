from project_code.my_maths import \
    select_from_matrix as select, \
    trigonometry as trig

from project_code import pixel_table


def sobel_calculation(matrix):
    horizontal = matrix[0][0].value + 2 * matrix[0][1].value + matrix[0][2].value \
                 - matrix[2][0].value - 2 * matrix[2][1].value - matrix[2][2].value
    vertical = -matrix[0][0].value - 2 * matrix[1][0].value - matrix[2][0].value \
                 + matrix[0][2].value + 2 * matrix[1][2].value + matrix[2][2].value
    return horizontal * 0.125, vertical * 0.125


def run_sobel_edge_detection(value_table: pixel_table.PixelTable) -> None:
    """"""
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
            edge_orientation = trig.calculate_angle_sobel(horizontal_strength, vertical_strength)

            image_pixels[row_index][column_index].cache = total_strength
            image_pixels[row_index][column_index].orientation = trig.round_angle(edge_orientation)

    value_table.set_new_pixel_values()
