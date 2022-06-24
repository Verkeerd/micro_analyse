import numpy
import numpy as np
from project_code.my_maths import select_from_matrix as select, mutate_matrix as mutate


def inner_product(vector_0: np.ndarray, vector_1: np.ndarray) -> np.ndarray:
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
