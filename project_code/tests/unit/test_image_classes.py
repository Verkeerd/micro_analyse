from project_code.image_manipulation.classes import \
    basic_shapes as shapes, \
    edge as edges, \
    pixel as pix, \
    pixel_table as tables

import unittest
from PIL import Image
import numpy as np

test_image_circle = "..\\project_code\\tests\\test_circles.png"


class TestBasicShapes(unittest.TestCase):
    """"""

    def test_construction_circle(self):
        a_circle = shapes.Circle(2, 1, 4)
        self.assertEqual(a_circle.center, (1, 4))
        self.assertEqual(a_circle.radius, 2)


class TestPixel(unittest.TestCase):
    """"""
    def test_construction_pixel(self):
        pixel_a = pix.GrayPixel((100, 100, 100))
        pixel_b = pix.GrayPixel((100, 100, 100, 15))
        pixel_c = pix.GrayPixel(248)
        pixel_d = pix.GrayPixel((10, 20, 30))

        # Testing perator overloading
        self.assertIsNone(pixel_a.cache)
        self.assertIsNone(pixel_a.orientation)
        self.assertEqual(pixel_a.value, 100)

        self.assertEqual(pixel_b.value, 100)
        self.assertEqual(pixel_c.value, 248)
        self.assertEqual(pixel_d.value, 18)

    def test_arithmatic_operators(self):
        pixel_a = pix.GrayPixel(100)
        pixel_b = pix.GrayPixel(100)

        self.assertEqual(pixel_a + pixel_b, 200)
        self.assertEqual(pixel_a + 9, 109)
        self.assertEqual(pixel_a + 94.6, 194.6)

        self.assertEqual(pixel_a * pixel_b, 10000)
        self.assertEqual(pixel_a * 0.5, 50)
        self.assertEqual(pixel_a * 2, 200)

    def comparison_operators(self):
        pixel_a = pix.GrayPixel(100)
        pixel_b = pix.GrayPixel(100)
        pixel_c = pix.GrayPixel(120)

        self.assertEqual(pixel_a == pixel_b, True)
        self.assertEqual(pixel_a == 100, True)
        self.assertEqual(pixel_a == 100.1, False)
        self.assertEqual(pixel_a == pixel_c, False)

        self.assertEqual(pixel_a != pixel_b, False)
        self.assertEqual(pixel_a != 100, False)
        self.assertEqual(pixel_a != 100.1, True)
        self.assertEqual(pixel_a != pixel_c, True)

        self.assertEqual(pixel_a < pixel_b, False)
        self.assertEqual(pixel_a < 100, False)
        self.assertEqual(pixel_a < 100.1, True)
        self.assertEqual(pixel_a < pixel_c, True)
        self.assertEqual(pixel_a < 99, False)

        self.assertEqual(pixel_a > pixel_b, False)
        self.assertEqual(pixel_a > 100, False)
        self.assertEqual(pixel_a > 100.1, False)
        self.assertEqual(pixel_a > pixel_c, False)
        self.assertEqual(pixel_a > 99, True)
        self.assertEqual(pixel_c > pixel_b, True)

    def test_set_new_value(self):
        pixel_a = pix.GrayPixel(100)
        pixel_a.set_new_value()

        self.assertEqual(pixel_a.value, 100)

        pixel_a.cache = 5
        pixel_a.set_new_value()
        self.assertEqual(pixel_a.value, 5)
        self.assertIsNone(pixel_a.cache)

    def test_turn_off(self):
        pixel_a = pix.GrayPixel(100)
        pixel_a.orientation = 20
        pixel_a.cache = 20

        pixel_a.turn_off()

        self.assertEqual(pixel_a.value, 0)
        self.assertIsNone(pixel_a.orientation)
        # cache is unchanged.
        self.assertEqual(pixel_a.cache, 20)

    def test_is_on_and_off(self):
        pixel_a = pix.GrayPixel(100)
        pixel_b = pix.GrayPixel(100)

        pixel_b.value = 0
        pixel_b.cache = 20

        self.assertTrue(pixel_a.is_on())
        self.assertFalse(pixel_a.is_off())

        self.assertFalse(pixel_b.is_on())
        self.assertTrue(pixel_b.is_off())

        pixel_b.orientation = 0.1

        self.assertTrue(pixel_b.is_on())
        self.assertFalse(pixel_b.is_off())

    def test_copy_colour_variant(self):
        pixel_a = pix.GrayPixel(200)
        self.assertEqual(pixel_a.copy_colour_variant(), (200, 200, 200))

        pixel_a.value = 19.9
        self.assertEqual(pixel_a.copy_colour_variant(), (19, 19, 19))

    def test_copy_orientation_as_colour(self):
        pixel_a = pix.GrayPixel(100)

        angle_colours = pix.angle_colour_dict

        for angle, colour_angle in angle_colours.items():
            for check_orientation in (angle - 0.01, angle):
                pixel_a.orientation = check_orientation
                self.assertEqual(pixel_a.copy_orientation_as_colour(), colour_angle)
            pixel_a.orientation = angle + 0.01
            self.assertNotEqual(pixel_a.copy_orientation_as_colour(), colour_angle)


class TestEdge(unittest.TestCase):
    """"""

    def test_construction_edge(self):
        an_edge = edges.ContinuousEdge()
        self.assertEqual(an_edge.pixels, [])

        a_pixel = pix.GrayPixel(200)
        an_edge = edges.ContinuousEdge(a_pixel)
        self.assertEqual(an_edge.pixels, [a_pixel])

        # Other objects than pixels, like integers, can also be given.
        an_edge = edges.ContinuousEdge(150)
        self.assertEqual(an_edge.pixels, [150])

        an_edge = edges.ContinuousEdge(15.1)
        self.assertEqual(an_edge.pixels, [15.1])

    def test_add_pixel(self):
        an_edge = edges.ContinuousEdge()
        self.assertEqual(an_edge.pixels, [])

        a_pixel = pix.GrayPixel(200)
        an_edge.add_pixel(a_pixel)
        self.assertEqual(an_edge.pixels, [a_pixel])

        another_pixel = pix.GrayPixel(144)
        an_edge.add_pixel(another_pixel)
        self.assertEqual(an_edge.pixels, [a_pixel, another_pixel])

    def test_fill_pixels(self):
        pixel_a = pix.GrayPixel(10)
        pixel_b = pix.GrayPixel(20)
        pixel_c = pix.GrayPixel(0)
        pixel_d = pix.GrayPixel(0)
        pixel_e = pix.GrayPixel(0)
        pixel_f = pix.GrayPixel(60)
        pixel_g = pix.GrayPixel(0)
        pixel_h = pix.GrayPixel(0)
        pixel_i = pix.GrayPixel(90)

        a_pixel_matrix = np.array([[pixel_a, pixel_b, pixel_c],
                                   [pixel_d, pixel_e, pixel_f],
                                   [pixel_g, pixel_h, pixel_i]])

        an_edge = edges.ContinuousEdge(pixel_a)
        an_edge.fill_missing_pixels(np.array(a_pixel_matrix), 0, 0, 1)

        self.assertEqual(an_edge.pixels[0], pixel_a)
        self.assertEqual(an_edge.pixels[0].cache, 1)

        self.assertEqual(an_edge.pixels[1], pixel_b)
        self.assertEqual(an_edge.pixels[1].cache, 1)

        self.assertEqual(an_edge.pixels[2], pixel_f)
        self.assertEqual(an_edge.pixels[3], pixel_i)

        # Does not record pixels more than once.
        a_pixel_matrix = np.array([[pixel_a, pixel_e, pixel_c],
                                   [pixel_d, pixel_b, pixel_f],
                                   [pixel_g, pixel_h, pixel_i]])

        another_edge = edges.ContinuousEdge(pixel_f)
        another_edge.fill_missing_pixels(a_pixel_matrix, 0, 2, 1)

        self.assertEqual(another_edge.pixels[0], pixel_f)
        self.assertEqual(len(another_edge.pixels), 1)

        for pixel_row in a_pixel_matrix:
            for pixel in pixel_row:
                pixel.cache = None

        yet_another_edge = edges.ContinuousEdge(pixel_b)
        yet_another_edge.fill_missing_pixels(a_pixel_matrix, 1, 1)
        # Finds the pixels again after the cache has been cleared. Searches left top first and goes up to down.
        self.assertEqual(yet_another_edge.pixels[0], pixel_b)
        self.assertEqual(yet_another_edge.pixels[1], pixel_a)

    def test_turn_off(self):
        pixel_a = pix.GrayPixel(10)
        pixel_b = pix.GrayPixel(20)
        pixel_c = pix.GrayPixel(30)
        pixel_d = pix.GrayPixel(40)

        an_edge = edges.ContinuousEdge(start_pixel=pixel_a)
        an_edge.add_pixel(pixel_b)
        an_edge.add_pixel(pixel_c)
        an_edge.add_pixel(pixel_d)

        self.assertEqual(an_edge.pixels, [10, 20, 30, 40])

        an_edge.turn_off()

        self.assertEqual(an_edge.pixels, [0, 0, 0, 0])
        self.assertEqual(pixel_a, 0)
        self.assertEqual(pixel_b, 0)
        self.assertEqual(pixel_c, 0)
        self.assertEqual(pixel_d, 0)

        an_edge.turn_off()

        self.assertEqual(an_edge.pixels, [0, 0, 0, 0])

    def validate(self):
        thresholds = [-30, 0, 11, 20, 39.9, 40]

        pixel_a = pix.GrayPixel(10)
        pixel_b = pix.GrayPixel(20)
        pixel_c = pix.GrayPixel(30)
        pixel_d = pix.GrayPixel(40)

        an_edge = edges.ContinuousEdge(start_pixel=pixel_a)
        an_edge.add_pixel(pixel_b)
        an_edge.add_pixel(pixel_c)
        an_edge.add_pixel(pixel_d)

        for threshold in thresholds:
            an_edge.validate(threshold)
            self.assertEqual(an_edge.pixels, [10, 20, 30, 40])

        an_edge.validate(40.1)
        self.assertEqual(an_edge.pixels, [0, 0, 0, 0])
        self.assertEqual(pixel_a, 0)
        self.assertEqual(pixel_b, 0)
        self.assertEqual(pixel_c, 0)
        self.assertEqual(pixel_d, 0)


class TextPixelTable(unittest.TestCase):
    def test_construction_pixel_table(self):
        with self.assertRaises(ValueError):
            tables.PixelTable(-1, 1)
            tables.PixelTable(1, -1)

        a_pixel_table = tables.PixelTable(3, 3)
        self.assertEqual(a_pixel_table.pixels.shape, (3, 3))

        a_pixel_table = tables.PixelTable(30, 60)
        self.assertEqual(a_pixel_table.pixels.shape, (60, 30))

    def test_fill_with_image(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))

        for pixel_row in a_pixel_table.pixels:
            for pixel in pixel_row:
                pixel.value = 255
        for i in range(10):
            for j in range(10):
                self.assertEqual(a_pixel_table.pixels[i][j], 255)

    def test_set_new_values(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))

        for i in range(10):
            for j in range(10):
                a_pixel_table.pixels[i][j].cache = 2
                a_pixel_table.pixels[i][j].orientation = 2

        a_pixel_table.set_new_pixel_values()

        for i in range(10):
            for j in range(10):
                self.assertEqual(a_pixel_table.pixels[i][j], 2)
                self.assertIsNone(a_pixel_table.pixels[i][j].cache)
                self.assertEqual(a_pixel_table.pixels[i][j].orientation, 2)

    def test_clear_cache(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))

        a_pixel_table.pixels[0][0].cache = 0
        a_pixel_table.pixels[0][1].cache = -63
        a_pixel_table.pixels[0][2].cache = 535
        a_pixel_table.pixels[0][3].cache = "hello"
        a_pixel_table.pixels[0][4].cache = [1, 2]
        a_pixel_table.pixels[0][5].cache = {1: (1, 2)}
        a_pixel_table.pixels[0][6].cache = (1, 1)

        a_pixel_table.clear_cache()

        for i in range(7):
            self.assertIsNone(a_pixel_table.pixels[0][i].cache)

    def test_turn_off_border(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))

        a_pixel_table.pixels[0][0].orientation = -1
        a_pixel_table.pixels[0][0].cache = -1

        a_pixel_table.turn_off_borders(border_width=3)

        self.assertEqual(a_pixel_table.pixels[0][0].cache, -1)

        for i in range(3):
            for j in range(10):
                self.assertEqual(a_pixel_table.pixels[i][j], 0)
                self.assertIsNone(a_pixel_table.pixels[i][j].orientation)

        for i in range(3, 7):
            for j in range(3):
                self.assertEqual(a_pixel_table.pixels[i][j], 0)
                self.assertIsNone(a_pixel_table.pixels[i][j].orientation)

    def test_get_active_pixels(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))

        original_pixels = a_pixel_table.pixels.copy()
        active_pixels = a_pixel_table.get_active_pixels()

        active_index = 0
        for row in original_pixels:
            for element in row:
                if element.value == 0 and element.orientation is None:
                    self.assertEqual(element, active_pixels[active_index])
                    active_index += 1

        for active_pixel in active_pixels:
            active_pixel.value = 300
            active_pixel.cache = 3
            active_pixel.orientation = 1

        for row in original_pixels:
            for element in row:
                if element.is_on():
                    self.assertEqual(element, 300)
                    self.assertEqual(element.cache, 3)
                    self.assertEqual(element.orientation, 1)

    def test_get_luminosity(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))
        value_active_pixels = a_pixel_table.get_luminosity_active_pixels()

        self.assertAlmostEqual(value_active_pixels[0], 24)
        self.assertAlmostEqual(value_active_pixels[1], 24)
        self.assertAlmostEqual(value_active_pixels[2], 24)

        for value in value_active_pixels:
            if value.orientation is not None:
                self.assertNotEqual(value, 0)

    def test_rgb_copy(self):
        test_image_edges = "test_image_edges.png"

        a_pixel_table = tables.PixelTable(10, 10)
        a_pixel_table.fill_with_image(Image.open(test_image_edges))
        an_rbg_pixel_table = a_pixel_table.rgb_copy()

        self.assertEqual(an_rbg_pixel_table.shape[:-1], a_pixel_table.pixels.shape)
        self.assertEqual(an_rbg_pixel_table.shape[-1], 3)
        for i in range(3):
            self.assertEqual(an_rbg_pixel_table[3][5][i], a_pixel_table.pixels[3][5].copy_colour_variant()[i])
            self.assertEqual(an_rbg_pixel_table[4][4][i], a_pixel_table.pixels[4][4].copy_colour_variant()[i])
            self.assertEqual(an_rbg_pixel_table[0][0][i], a_pixel_table.pixels[0][0].copy_colour_variant()[i])
