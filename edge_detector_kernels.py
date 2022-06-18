import numpy as np
import lineair_algebra as lin_alg


def horizontal_sobel_kernel(size=5):
    """
    Creates a horizontal sobel kernel


    Parameters
    ----------
    size: int

    Returns
    -------
    numpy.ndarray
        The horizontal sobel kernel
    """
    sobel_kernel = np.zeros((size, size))
    kernel_radius = size // 2
    for row in range(kernel_radius):
        standard_weight = kernel_radius - row
        sobel_kernel[row][kernel_radius] = -standard_weight * 2
        sobel_kernel[- (row + 1)][kernel_radius] = standard_weight * 2
        for column in range(kernel_radius):
            sobel_kernel[row][column] = -standard_weight
            sobel_kernel[row][-(1 + column)] = -standard_weight

            sobel_kernel[- (row + 1)][column] = standard_weight
            sobel_kernel[- (row + 1)][-(1 + column)] = standard_weight

    return sobel_kernel


def vertical_sobel_kernel(size=5):
    """"""
    return lin_alg.transpose(horizontal_sobel_kernel(size=size))
