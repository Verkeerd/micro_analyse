import project_code.image_manipulation.kernels.blurs as blur

from project_code.my_maths import \
    lineair_algebra as lin_alg, \
    select_from_matrix as select

import numpy as np


def apply_kernel(sub_image, kernel):
    """
    Applies a kernel to a pixel.

    This function applies a kernel to a pixel. It calculates the hadamard product of the kernel and pixel with its
    surroundings. After this it takes the total sum of the hadamard product.

    Parameters
    ----------
    sub_image : numpy.ndarray
        The pixel we want to apply the kernel to, inside a matrix as center slot. The rest of the matrix is filled with
        pixels that are within the range of the kernel radius.
    kernel : numpy.ndarray
        The kernel to apply.

    Returns
    -------
    int
        The value of the pixel after the kernel has been applied.
    """
    sub_image = np.reshape(sub_image, -1)
    kernel = np.reshape(kernel, -1)
    return lin_alg.inner_product(sub_image, kernel)


def gauss_blur(value_table, kernel_size):
    image_pixels = value_table.pixels

    gaussian_kernel = blur.gaussian_kernel(kernel_size)
    kernel_radius = kernel_size // 2
    height, width = image_pixels.shape

    for row_index in range(kernel_radius, height - kernel_radius):
        for column_index in range(kernel_radius, width - kernel_radius):
            pixel_and_surrounding = select.get_sub_matrix(image_pixels,
                                                          row_index - kernel_radius,
                                                          column_index - kernel_radius,
                                                          size=kernel_size)

            new_pixel_value = apply_kernel(pixel_and_surrounding, gaussian_kernel)
            image_pixels[row_index][column_index].cache = int(new_pixel_value)

    value_table.set_new_pixel_values()
