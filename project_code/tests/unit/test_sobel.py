from project_code.image_manipulation.classes import pixel as pixel_classes
from project_code.image_manipulation import sobel_edge_detector as sobel

import unittest
import numpy as np


class TestSobelEdgeDetection(unittest.TestCase):
    """"""
    def SobelCalculation(self):
        pixels_3_3 = np.array([[pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)]])

        pixels_5_5 = np.array([[pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)],
                               [pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10), pixel_classes.GrayPixel(10)]])

        self.assertEqual(sobel.sobel_calculation(pixels_3_3), 0)
        self.assertEqual(sobel.sobel_calculation(pixels_5_5, 5), 0)

        for i in range(3):
            pixels_3_3[0][i].value = 255
            pixels_3_3[2][i].value = 255

        self.assertEqual(sobel.sobel_calculation(pixels_3_3), 0)

        for i in range(3):
            pixels_3_3[0][i].value = 10

        self.assertEqual(sobel.sobel_calculation(pixels_3_3), -112.5)
