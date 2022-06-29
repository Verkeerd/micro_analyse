from project_code.image_manipulation import hough_circle_transform as hough

import unittest


class TestHoughCircleTransform(unittest.TestCase):
    def test_construct_3d_space(self):
        a_dict = {2: [(2, 3, 2), (5, 1, 6), (3, 6, 4)], 3: [(3, 3, 1), (2, 3, 5), (6, 5, 9)], 4: [3, 3, 100]}

        space3d = hough.constructs_magnitudes_in_3d_space(a_dict, 2, 2, 2, 1, True)
        print(space3d)
        self.assertEqual(space3d.shape, (2, 2, 2))
        self.assertEqual(list(space3d[0]), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
