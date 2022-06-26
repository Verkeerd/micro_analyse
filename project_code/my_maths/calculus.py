import numpy as np


def local_maximum_1d(local_vector: np.ndarray) -> int:
    """
    Calculates the index of the local maximum.

    Parameters
    ----------
    local_vector : numpy.ndarray
        Row of values in a vector.

    Returns
    -------
    int
        Index of the local maximum.
    """
    maximum = local_vector[0]
    index = 0
    for pixel_index, edge_pixel in enumerate(local_vector[1:]):
        if edge_pixel > maximum:
            index = pixel_index + 1
            maximum = edge_pixel
    return index


def local_maximum_2d_cache(local_matrix):
    """
    Calculates the index of the local maximum in a 2d matrix.
    The matrix has to contain a datatype containing a cache attribute, like Grey Pixel.
    The local maximum pixel when comparing their cache attribute is calculated and so is its index.

    Parameters
    ----------
    local_matrix: np.ndarray
        The local matrix we are searching for the maximum value in terms of cache.

    Returns
    -------
    tuple: (int, int)
        Index of the local maximum (y, x).
    """
    maximum_index = (0, 0)
    maximum = local_matrix[0, 0].cache
    for row_index, row in enumerate(local_matrix):
        for column_index, current_value in enumerate(row):
            current_value = current_value.cache
            if current_value is None:
                continue
            if current_value > maximum:
                maximum_index = (row_index, column_index)
                maximum = current_value

    return maximum_index
