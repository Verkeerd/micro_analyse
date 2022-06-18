import numpy as np
import lineair_algebra as lin_alg
import math


def gaussian_formula(x, radius, sigma):
    """Calculates x for"""
    # source: https://mathworld.wolfram.com/GaussianFunction.html
    x -= radius
    return math.exp((x**2 / (2 * sigma ** 2)) * -1) / sigma * math.sqrt(2 * math.pi)


def gaussian_kernel(size=5):
    """"""
    if size % 2 != 1:
        print("gaussiant filter must have an uneven size.")
    np.zeros((size, size))

    # Source: moooeeeep, Nov 20, 2011,
    # https://stackoverflow.com/questions/8204645/implementing-gaussian-blur-how-to-calculate-convolution-matrix-kernel
    kernel_radius = size // 2
    sigma = size / 2 / 2

    # compute the actual kernel elements
    gaussian_1d = [gaussian_formula(x, kernel_radius, sigma) for x in range(2 * kernel_radius + 1)]

    kernel_2d = [[row_weight * column_weight for row_weight in gaussian_1d] for column_weight in gaussian_1d]

    # normalize the kernel elements
    sum_kernel = sum([sum(row) for row in kernel_2d])
    kernel_2d = [[x / sum_kernel for x in row] for row in kernel_2d]

    return np.resize(kernel_2d, (size, size))
