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
    """Takes a matrix(ndarray) as input. Returns the diagonal of the matrix."""
    if rl:
        flipped_matrix = np.fliplr(matrix.copy())
        return np.diag(flipped_matrix)
    return np.diag(matrix)


def secure_matrix(an_array: np.ndarray, column_vector=False) -> np.ndarray:
    """
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


def get_sub_matrix(mother_matrix, x_start, y_start, size=5):
    """"""
    sub_matrix_view = mother_matrix[x_start: x_start+size, y_start: y_start+size]

    return sub_matrix_view.copy()


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
    if angle == 0:
        return extract_row(matrix_with_edge, kernel_radius)
    if angle == 45:
        return extract_diagonal(matrix_with_edge, rl=True)
    if angle == 90:
        return extract_column(matrix_with_edge, kernel_radius)
    if angle == 135:
        return extract_diagonal(matrix_with_edge)


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
        column_vector = extract_column(matrix, column_index)
        # Assigns the column vector as rowvector to the transposition.
        transposition_matrix[column_index] = column_vector

    return transposition_matrix


def rounded_angle(angle):
    """
    Rounds an angle.

    This function rounds an angle to the closest of four angles:
    The vertical-, horizontal- or one of the two diagonal directions.

    Parameters
    ----------
    angle: float
        The angle.

    Returns
    -------
    int
        The rounded angle.
    """
    if angle <= -0.225:
        return rounded_angle(angle + 1.8)
    if angle <= 0.225:
        return 0
    if angle <= 0.675:
        return 45
    if angle <= 1.125:
        return 90
    if angle <= 1.575:
        return 135
    return rounded_angle(angle-1.8)


def inner_product(vector_0: np.ndarray, vector_1: np.ndarray) -> np.ndarray:
    """
    Calculates the inner product of two vectors.

    Parameters
    ----------
    vector_0 : numpy.ndarray
        A vector
    vector_1 : numpy.ndarray
        A vector

    Raises
    ------
    numpy.AxisError
        One or both vectors are a multidimensional matrices.
    numpy.AxisError
        Vectors don't exist in the same space.

    Returns
    -------
    int
        The inner product of the two vectors
    """
    if len(vector_0.shape) != 1 or len(vector_1.shape) != 1:
        raise np.AxisError("Give vectors, not matrices.")
    vector_0_length = len(vector_0)
    vector_1_length = len(vector_1)
    if vector_0_length != vector_1_length:
        raise np.AxisError("Vector 1 of x axis", vector_0_length,
                           "is not compatible with vector 2 of x axis", vector_1_length)

    return inner_product_no_guards(vector_0, vector_1)


def inner_product_no_guards(vector_0: np.ndarray, vector_1: np.ndarray) -> np.ndarray:
    """
    Calculates the inner product of two vectors.

    Parameters
    ----------
    vector_0 : numpy.ndarray
        A vector
    vector_1 : numpy.ndarray
        A vector

    Returns
    -------
    int
        The inner product of the two vectors
    """
    # Copies a vector to use as the resulting vector we want to return.
    products = vector_0.copy()

    # Takes the product of the corresponding coordinates in the vectors.
    for i in range(len(vector_0)):
        products[i] = vector_0[i] * vector_1[i]

    # returns the sum of all vector products
    return sum(products)


def matrix_product(origin: np.ndarray, translations: np.ndarray) -> np.ndarray:
    """
    Calculates the product of the two matrices.

    This function does the following for every row vector in origin:
        For every translation (column) vector in translations,
            Take the inner product between the translation vector and the row vector in
            origin.
            Place this inner product in a new matrix, in the same row as (the row vector)
            in origin and in same column as (the translation vector) in translations.

    Parameters
    ----------
    origin : numpy.ndarray
        The origin matrix.
    translations : numpy.ndarray
        The translation matrix.

    Returns
    -------
    numpy ndarray
        The product of the two matrices (ndarray).
    """
    # Resize translations and/or origin if they are a vector
    origin = secure_matrix(origin)
    translations = secure_matrix(translations, column_vector=True)

    if origin.shape[1] != translations.shape[0]:
        raise np.AxisError('origin with x axis of', origin.shape[1],
                           'and translations with y axis of', translations.shape[0],
                           'are not compatible.')

    # Creates an array for the resulting matrix
    result = np.empty((origin.shape[0], translations.shape[1]))

    # For every row vector in origin
    for row_index, row_vector in enumerate(origin):
        # For every translation (column) vector in translation
        for column_index in range(translations.shape[1]):
            # Extracts the translation vector.
            translation_vector = extract_column(translations, column_index)
            # Calculates the inner product between the row vector and the translation vector.
            result[row_index][column_index] = inner_product_no_guards(row_vector, translation_vector)

    return result


def hadamard_product_no_guard(origin, translation):
    """"""
    return np.multiply(origin, translation)
