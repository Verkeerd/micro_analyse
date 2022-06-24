import numpy as np


def extract_column(matrix: np.ndarray, column_index: int) -> np.ndarray:
    """
    Takes a matrix (ndarray) and a column_index (int) as input.
    Creates an array with the column vector on the given column index of the matrix.
    Returns this array (ndarray).
    """
    # source: Adam Smith,
    # https://www.adamsmith.haus/python/answers/how-to-extract-a-column-from-a-numpy-array-in-python
    return matrix[:, column_index]


def extract_row(matrix, row_index):
    """
    Takes a matrix (ndarray) and a row_index (int) as input.
    Creates an array with the row vector on the given row index of the matrix.
    Returns this array (ndarray).
    """
    return matrix[row_index]


def extract_diagonal(matrix, rl=False):
    """
    Computes the diagonal or trans-diagonal vector of a matrix.

    Parameters
    ----------
    matrix : numpy.ndarray
        A matrix
    rl : bool
        False for diagonal, True for trans-diagonal

    Returns
    -------

    """
    if rl:
        flipped_matrix = np.fliplr(matrix.copy())
        return np.diag(flipped_matrix)
    return np.diag(matrix)


def get_sub_matrix(mother_matrix, x_start, y_start, size=5):
    """"""
    sub_matrix_view = mother_matrix[x_start: x_start+size, y_start: y_start+size]

    return sub_matrix_view


def get_perpendicular_vector(matrix_with_edge, angle, kernel_radius):
    """
    Get the vector perpendicular to the edge.

    This function extracts the vector inside ``matrix_with_edge`` that runs perpendicular to the edge inside the matrix.

    Parameters
    ----------
    matrix_with_edge : np.ndarray
        The pixel matrix containing the edge and surrounding pixels.
    angle : int
        The angle perpendicular to the edge.
    kernel_radius : int
        The radius of ``matrix_with_edge``

    Returns
    -------

    """
    if angle == 0 or angle == 180:
        return extract_row(matrix_with_edge, kernel_radius)
    if angle == 45 or angle == 225:
        return extract_diagonal(matrix_with_edge, rl=True)
    if angle == 90 or angle == 270:
        return extract_column(matrix_with_edge, kernel_radius)
    if angle == 135 or angle == 315:
        return extract_diagonal(matrix_with_edge)


def add_adjacent_column_index_right(row_index, column_index):
    return row_index, column_index + 1


def add_adjacent_column_index_right_below(row_index, column_index):
    return row_index + 1, column_index + 1


def add_adjacent_row_indexes_below(row_index, column_index):
    for i in range(column_index - 1, column_index + 1):
        return
