from project_code.my_maths import \
    mutate_matrix as mutate, \
    select_from_matrix as matrix_select, \
    lineair_algebra as lin_alg, \
    calculus as calc, \
    trigonometry as trig

import unittest
import numpy as np


class TestMutateMatrix(unittest.TestCase):
    """"""

    def test_transpose(self):
        a_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        transposed_matrix = mutate.transpose(a_matrix)
        wanted_results = np.transpose(a_matrix)
        for y in range(3):
            for x in range(3):
                self.assertEqual(transposed_matrix[x][y], wanted_results[x][y])


class TestSelectFromMatrix(unittest.TestCase):
    """"""
    def test_extract_vectors(self):
        """"""
        a_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(list(matrix_select.extract_column(a_matrix, 1)), [2, 5, 8])
        self.assertEqual(list(matrix_select.extract_column(a_matrix, -1)), [3, 6, 9])

        self.assertEqual(list(matrix_select.extract_row(a_matrix, 1)), [4, 5, 6])
        self.assertEqual(list(matrix_select.extract_row(a_matrix, -1)), [7, 8, 9])

        with self.assertRaises(IndexError):
            matrix_select.extract_column(a_matrix, 3)
            matrix_select.extract_column(a_matrix, 3)

        self.assertEqual(list(matrix_select.extract_diagonal(a_matrix)), [1, 5, 9])
        self.assertEqual(list(matrix_select.extract_diagonal(a_matrix, rl=True)), [3, 5, 7])

    def test_sub_matrix(self):
        a_matrix = np.array([[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10], [10, 11, 12, 13]])

        sub_matrix_a = matrix_select.get_sub_matrix(a_matrix, 1, 1, 2)
        result_a = np.array([[5, 6], [8, 9]])
        for y in range(2):
            for x in range(2):
                self.assertEqual(sub_matrix_a[y][x], result_a[y][x])

        result_b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        sub_matrix_b = matrix_select.get_sub_matrix(a_matrix, 0, 0, 3)
        for y in range(3):
            for x in range(3):
                self.assertEqual(sub_matrix_b[y][x], result_b[y][x])

        # A sub-matrix that is partially out of bounds in the monther matrix will cast to the size that fits.
        result_c = [[9, 10], [12, 13]]
        sub_matrix_c = matrix_select.get_sub_matrix(a_matrix, 2, 2, 4)

        self.assertEqual(sub_matrix_c.size, 4)
        for y in range(2):
            for x in range(2):
                self.assertEqual(sub_matrix_c[y][x], result_c[y][x])
        # A sub-matrix that is completely out of bounds in the monther matrix will be an empty array.
        self.assertEqual(matrix_select.get_sub_matrix(a_matrix, 4, 4, 2).size, 0)

    def test_vector_as_per_angle(self):
        # Matrix used for testing.
        a_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        # Wanted results.
        the_row = [4, 5, 6]
        the_column = [2, 5, 8]
        diag = [1, 5, 9]
        diag_rl = [3, 5, 7]

        # Checks all angle boundaries
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, -2, 1)), the_column)
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, -1.5, 1)), the_column)

        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, -1.49, 1)), diag)
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, -0.5, 1)), diag)

        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, -0.49, 1)), the_row)
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, 0.5, 1)), the_row)

        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, 0.51, 1)), diag_rl)
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, 1.5, 1)), diag_rl)

        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, 1.51, 1)), the_column)
        self.assertEqual(list(matrix_select.vector_as_per_angle(a_matrix, 2, 1)), the_column)

        # The function does not return anything when the angle is bigger than two (pi radius).
        self.assertIsNone(matrix_select.vector_as_per_angle(a_matrix, 2.1, 1))
        # It also does not return anything when the angle is smaller than 2 (pi radius).
        self.assertIsNone(matrix_select.vector_as_per_angle(a_matrix, -2.1, 1))

        # Raises an index error when the area asked for is out of bounds for the matrix.
        with self.assertRaises(IndexError):
            matrix_select.vector_as_per_angle(a_matrix, 0, 3)


class TestLineairAlgebra(unittest.TestCase):
    def test_inner_product(self):
        a_vector = np.array([1, 2])
        another_vector = np.array([2, 4])
        self.assertEqual(lin_alg.inner_product(a_vector, another_vector), np.dot(a_vector, another_vector))


class TestTrigonometry(unittest.TestCase):
    """"""
    def test_calculate_hypotenuse(self):
        self.assertEqual(trig.calculate_hypotenuse(3, 4), 5)
        self.assertEqual(trig.calculate_hypotenuse(-3, 4), 5)
        self.assertEqual(trig.calculate_hypotenuse(3, -4), 5)
        self.assertEqual(trig.calculate_hypotenuse(-3, -4), 5)

        self.assertAlmostEqual(trig.calculate_hypotenuse(6.2, 2.1), 6.545991139621257, delta=0.001)
        self.assertAlmostEqual(trig.calculate_hypotenuse(-6.2, 2.1), 6.545991139621257, delta=0.001)
        self.assertAlmostEqual(trig.calculate_hypotenuse(6.2, -2.1), 6.545991139621257, delta=0.001)
        self.assertAlmostEqual(trig.calculate_hypotenuse(-6.2, -2.1), 6.545991139621257, delta=0.001)

        self.assertEqual(trig.calculate_hypotenuse(0, -4), 4)
        self.assertEqual(trig.calculate_hypotenuse(0, 4), 4)

    def test_approximate_hypotenuse(self):
        self.assertEqual(trig.approximate_hypotenuse(3, 4), 7)
        self.assertEqual(trig.approximate_hypotenuse(-3, 4), 7)
        self.assertEqual(trig.approximate_hypotenuse(3, -4), 7)
        self.assertEqual(trig.approximate_hypotenuse(-3, -4), 7)

        self.assertEqual(trig.approximate_hypotenuse(6.2, 2.1), 8.3)
        self.assertEqual(trig.approximate_hypotenuse(-6.2, 2.1), 8.3)
        self.assertEqual(trig.approximate_hypotenuse(6.2, -2.1), 8.3)
        self.assertEqual(trig.approximate_hypotenuse(-6.2, -2.1), 8.3)

        self.assertEqual(trig.approximate_hypotenuse(0, -4), 4)
        self.assertEqual(trig.approximate_hypotenuse(0, 4), 4)

    def test_calculate_gradient_angle(self):
        self.assertAlmostEqual(trig.calculate_gradient_angle(4, 2), 0.4636476, delta=0.001)
        self.assertAlmostEqual(trig.calculate_gradient_angle(0.4, 0.3), 0.6435011, delta=0.001)
        self.assertAlmostEqual(trig.calculate_gradient_angle(-4, 2), -0.4636476, delta=0.001)
        self.assertAlmostEqual(trig.calculate_gradient_angle(0.4, -0.3), -0.6435011, delta=0.001)

    def new_xy_circumference_circle(self):
        """"""
        radii = [1, 5.4]
        angles = [0, 90, 132, 1, -1, 359, 361, -361]

        answers = [[(1.0,       0.0),       (0.0,       1.0),
                    (-0.66913,  0.74314),   (0.99984,   0.01745),
                    (0.99984,   -0.01745),  (0.99984,   -0.01745),
                    (0.99984,   0.01745),   (0.99984,   -0.01745)],

                   [(5.4,       0.0),       (0.0,       5.4),
                    (-3.6133,   4.012956),  (5.399136,  0.09423),
                    (5.399136,  -0.09423),  (5.399136,  -0.09423),
                    (5.399136,  0.09423),   (5.399136,  -0.09423)]]

        for first_index, radius in enumerate(radii):
            for second_index, angle in enumerate(angles):
                x, y = trig.new_xy_circumference_circle(angle, radius)
                x_result, y_result = answers[first_index][second_index]
                self.assertAlmostEqual(x, x_result)
                self.assertAlmostEqual(y, y_result)


class TestCalculus(unittest.TestCase):
    """"""
    def test_local_maximum_1d(self):
        self.assertEqual(calc.local_maximum_1d(np.array([1, 5, 6, 3])), (2, 6))
        self.assertEqual(calc.local_maximum_1d(np.array([-8, -2, -3])), (1, -2))
        self.assertEqual(calc.local_maximum_1d(np.array([0, 3, 3])), (1, 3))

    def test_local_maximum_2d_cache(self):
        index, maximum = calc.local_maximum_2d_cache(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        self.assertEqual(index, (2, 2))
        self.assertEqual(maximum, 9)

        index, maximum = calc.local_maximum_2d_cache(np.array([[1, 2, 6], [4, 5, 3]]))
        self.assertEqual(index, (2, 0))
        self.assertEqual(maximum, -2)

        index, maximum = calc.local_maximum_2d_cache(np.array([[0, 3, 3]]))
        self.assertEqual(index, (1, 0))
        self.assertEqual(maximum, 3)

        index, maximum = calc.local_maximum_2d_cache(np.array([[0], [3], [3]]))
        self.assertEqual(index, (0, 1))
        self.assertEqual(maximum, 3)

        index, maximum = calc.local_maximum_2d_cache(np.array([0, 3, 3]))
        self.assertEqual(index, (1, 0))
        self.assertEqual(maximum, 3)

    def test_local_maximum_3d(self):
        matrix_3d = np.array([[[1, 2, 3],
                               [4, 5, 6],
                               [7, 8, 9]],

                              [[2, 4, 6],
                               [8, 10, 12],
                               [14, 16, 18]],

                              [[1, 3, 6],
                               [9, 12, 15],
                               [18, 21, 24]]])

        self.assertEqual(calc.local_maximum_3d(matrix_3d), ((2, 2, 2), 24))
        matrix_3d[2][1][0] = 50
        self.assertEqual(calc.local_maximum_3d(matrix_3d), ((0, 1, 2), 50))

        matrix_3d *= -1

        self.assertEqual(calc.local_maximum_3d(matrix_3d), ((0, 0, 0), -1))
