import numpy as np
from project_code.my_maths import select_from_matrix as matrix_select


def secure_matrix(an_array: np.ndarray, column_vector=False) -> np.ndarray:
    """
    Creates a 2d array out of a 1d array.

    Takes an array (ndarray) as input.
    If the array is a vector, resizes it into a single column matrix and return this.
    If the array is a matrix, returns the matrix array unchanged.
    """
    if len(an_array.shape) == 1:
        if column_vector:  # we want a matrix with 1 column vector.
            return np.resize(an_array, (an_array.shape[0], 1))
        # not column_vector (we want a matrix with 1 row vector).
        return np.resize(an_array, (1, an_array.shape[0]))

    return an_array


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
