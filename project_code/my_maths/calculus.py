import numpy as np


def local_maximum_vector(intersection_edge: np.ndarray) -> int:
    """
    Checks if the center value in an array is the local maximum.

    Parameters
    ----------
    intersection_edge : numpy.ndarray
        Row of pixels of the edge, running perpendicular to the edge direction.
    radius : numpy.ndarray
        Radius of ``intersection_edge``
    Returns
    -------
    true
        The center pixel is a local maximum.
    false
        The center pixel is not a local maximum.
    """
    maximum = intersection_edge[0]
    index = 0
    for pixel_index, edge_pixel in enumerate(intersection_edge[1:]):
        if edge_pixel > maximum:
            index = pixel_index + 1
            maximum = edge_pixel
    return index


def local_maximum_matrix(matrix):
    """"""
    maximum_index = (0, 0)
    maximum = matrix[0, 0].cache
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            current_value = matrix[row_index, column_index].cache
            if current_value is None:
                continue
            if current_value > maximum:
                maximum_index = (row_index, column_index)
                maximum = current_value

    return maximum_index
