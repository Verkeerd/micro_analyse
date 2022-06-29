import numpy as np
import math


def gaussian_formula(x, sigma):
    """
    Calculates the value of x after the gaussian formula.

    This function applies the gaussian formula to a given number ``x``. The gaussian formula has been stretched by a
    given sigma.

    Parameters
    ----------
    x : float
        The function calculates the gaussian y value of this value.
    sigma : float
        The amount of range of the gaussian.

    Returns
    -------
    float
        The value of y at ``x`` for the gaussian formula of ``sigma``
    """
    # source: https://mathworld.wolfram.com/GaussianFunction.html
    return math.exp((x**2 / (2 * sigma ** 2)) * -1) / sigma * math.sqrt(2 * math.pi)


def gaussian_kernel(size=5):
    """
    Creates a 2d Gaussian kernel.

    Parameters
    ----------
    size : int
        Size of x and y. Has to be uneven.

    Returns
    -------
    numpy.ndarray
        The created (``size`` x ``size``) gaussian kernel.
    """
    if size % 2 != 1:
        raise ValueError("Gaussian filter must have an uneven size.")
    # Source: moooeeeep, Nov 20, 2011,
    # https://stackoverflow.com/questions/8204645/implementing-gaussian-blur-how-to-calculate-convolution-matrix-kernel
    kernel_radius = size // 2
    sigma = kernel_radius / 2

    # compute the actual kernel elements
    gaussian_1d = [gaussian_formula(x - kernel_radius, sigma) for x in range(size)]

    kernel_2d = [[row_weight * column_weight for row_weight in gaussian_1d] for column_weight in gaussian_1d]

    # normalize the kernel elements
    sum_kernel = sum([sum(row) for row in kernel_2d])
    kernel_2d = [[x / sum_kernel for x in row] for row in kernel_2d]

    return np.array(kernel_2d)
