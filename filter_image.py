import numpy as np
import lineair_algebra as lin_alg


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
    pixel_values_after_weight = lin_alg.hadamard_product_no_guard(sub_image, kernel)
    return sum([sum(row) for row in pixel_values_after_weight])


def local_maximum(matrix_with_edge, radius):
    """"""
    current_pixel = matrix_with_edge[radius][radius]
    angle = lin_alg.rounded_angle(current_pixel.orientation)
    print(angle)

    perpendicular_vector = lin_alg.get_perpendicular_vector(matrix_with_edge, angle, radius)

    if perpendicular_vector is None:
        return False
    else:
        print(perpendicular_vector)
    maximum = max(perpendicular_vector)
    if current_pixel.value != maximum:
        return False
    return True
