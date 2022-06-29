import numpy as np


def local_maximum_1d(local_vector: np.ndarray) -> tuple:
    """
    Calculates the local maximum.

    The maximum inside the local vector is calculated.

    Parameters
    ----------
    local_vector : numpy.ndarray
        A 1d vector with strengths.

    Returns
    -------
    tuple: (int, int)
        Index of the local maximum.
        Strength of the local maximum.
    """
    maximum = local_vector[0]
    current_index = 0
    for pixel_index, edge_pixel in enumerate(local_vector[1:]):
        if edge_pixel > maximum:
            current_index = pixel_index + 1
            maximum = edge_pixel
    return current_index, maximum


def local_maximum_2d_cache(local_matrix):
    """
    Calculates the index of the local maximum inside a 2d matrix.

    The matrix has to contain a datatype containing a cache attribute, like a Grey Pixel.
    The local maximum pixel, when comparing their cache attribute, is calculated and so is its index.

    Parameters
    ----------
    local_matrix: np.ndarray
        The 2d array with strengths.

    Returns
    -------
    tuple: ((int, int), int)
        Index of the local maximum (x, y).
        Strength of the local maximum.
    """
    current_index = (0, 0)
    maximum = local_matrix[0, 0].cache
    for row_index, row in enumerate(local_matrix):
        for column_index, current_value in enumerate(row):
            current_value_cache = current_value.cache
            if current_value_cache is None:
                continue
            if current_value_cache > maximum:
                current_index = (column_index, row_index)
                maximum = current_value_cache
            current_value.cache = None

    return current_index, maximum


def local_maximum_3d(local_3d_matrix):
    """
    Calculates the index of the local maximum in a 2d matrix.
    The matrix has to contain a datatype containing a cache attribute, like Grey Pixel.
    The local maximum pixel when comparing their cache attribute is calculated and so is its index.

    Parameters
    ----------
    local_3d_matrix: np.ndarray
        The 3d array with strengths.

    Returns
    -------
    tuple: ((int, int), int)
        Index of the local maximum (x, y, z).
        Strength of the local maximum.
    """
    z, y, x = local_3d_matrix.shape
    current_index = (0, 0, 0)
    current_maximum = local_3d_matrix[0][0][0]
    for height_index in range(z):
        for row_index in range(y):
            column_index, row_maximum = local_maximum_1d(local_3d_matrix[height_index][row_index])
            if row_maximum > current_maximum:
                current_maximum = row_maximum
                current_index = (column_index, row_index, height_index)

    return current_index, current_maximum
