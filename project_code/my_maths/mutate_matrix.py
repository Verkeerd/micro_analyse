from project_code.my_maths import select_from_matrix as matrix_select

import numpy as np


def transpose(matrix: np.ndarray) -> np.ndarray:
    """
    Computes the transposition of a matrix.

    This function computes the transposition of a matrix by inverting the row vectors and column vectors of the matrix.

    Parameters
    ----------
    matrix : numpy.ndarray
        A matrix.

    Returns
    -------
        The transposition of the matrix.
    """
    transposition_matrix = np.empty((matrix.shape[1], matrix.shape[0]))

    for column_index in range(matrix.shape[1]):
        # Extract the column on column index
        column_vector = matrix_select.extract_column(matrix, column_index)
        # Assigns the column vector as row vector to the transposition.
        transposition_matrix[column_index] = column_vector

    return transposition_matrix
