from project_code.image_manipulation.kernels import blurs as blur
from project_code.image_manipulation import standard_filters as stand_filter

import unittest
import numpy as np
from scipy import signal


class TestApplyKernel(unittest.TestCase):
    def test_normal_kernel(self):
        matrix = np.array([[1, 1, 1],
                           [2, 2, 2],
                           [3, 3, 3]])

        kernel_1 = np.array([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])

        kernel_2 = np.array([[6, 6, 6],
                                [5, 5, 5],
                                [4, 4, 4]])

        self.assertEqual(stand_filter.apply_kernel(matrix, kernel_1), 108)
        self.assertEqual(stand_filter.apply_kernel(matrix, kernel_2), 84)

        for x in range(kernel_2.shape[0]):
            for y in range(kernel_2.shape[1]):
                kernel_2[x][y] *= -1

        self.assertEqual(stand_filter.apply_kernel(matrix, kernel_2), -84)

    def test_asymmetric_kernel(self):
        matrix = np.array([[1, 1, 1],
                           [2, 2, 2]])

        kernel_1 = np.array([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])

        kernel_2 = np.array([[1, 2, 3],
                             [4, 5, 6]])

        with self.assertRaises(IndexError):
            stand_filter.apply_kernel(matrix, kernel_1)

        self.assertEqual(stand_filter.apply_kernel(matrix, kernel_2), 36)

        for x in range(kernel_2.shape[0]):
            for y in range(kernel_2.shape[1]):
                kernel_2[x][y] *= -1

        self.assertEqual(stand_filter.apply_kernel(matrix, kernel_2), -36)


class TestGaussian(unittest.TestCase):
    def test_gaussian_kernel(self):
        self.assertTrue(list(blur.gaussian_kernel(size=5)), list(signal.windows.gaussian(25, 2, True)))
        self.assertTrue(list(blur.gaussian_kernel(size=3)), list(signal.windows.gaussian(9, 1, True)))
