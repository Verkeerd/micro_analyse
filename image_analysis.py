from PIL import Image
import numpy as np
import math
import lineair_algebra as lin_alg
import filter_image as img_filter
import blur_kernels as blur
import edge_detector_kernels as edge_detection
import pixel
import matplotlib as plot


class ImageAnalysis(object):
    """"""
    def __init__(self, img):
        self.working_image = img
        self.pixel_table = np.zeros((self.working_image.height, self.working_image.width), dtype=pixel.GreyPixel)

    def method1(self):
        """"""
        return self.working_image.method1()

    def init_greyscale_pixel_table(self):
        """"""
        for row in range(self.working_image.height):
            for column in range(self.working_image.width):
                pixel_rgb = self.working_image.getpixel((column, row))
                pixel_value = pixel.GreyPixel(pixel_rgb)
                self.pixel_table[row][column] = pixel_value

    def set_new_pixel_values(self):
        """"""
        for row in self.pixel_table:
            for active_pixel in row:
                if active_pixel.new_value is not None:
                    active_pixel.value = active_pixel.new_value
                    active_pixel.new_value = None

    def apply_gaussian_blur(self, kernel_size=5):
        """"""
        print('Gauss.')
        kernel_radius = kernel_size // 2
        active_gaussian_kernel = blur.gaussian_kernel(kernel_size)
        for row in range(kernel_radius, self.working_image.height - kernel_radius):
            for column in range(kernel_radius, self.working_image.width - kernel_radius):
                pixel_and_surrounding = lin_alg.get_sub_matrix(self.pixel_table,
                                                               row - kernel_radius,
                                                               column - kernel_radius,
                                                               size=kernel_size)

                new_pixel_value = img_filter.apply_kernel(pixel_and_surrounding,
                                                          active_gaussian_kernel)

                self.pixel_table[row][column].new_value = new_pixel_value

        self.set_new_pixel_values()

    def apply_sobel_edge_detection(self, kernel_size=5):
        """"""
        print('Sobel.')
        horizontal_kernel = edge_detection.horizontal_sobel_kernel()
        vertical_kernel = lin_alg.transpose(horizontal_kernel)
        kernel_radius = kernel_size // 2
        for row in range(kernel_radius, self.working_image.height - kernel_radius):
            for column in range(kernel_radius, self.working_image.width - kernel_radius):
                pixel_and_surrounding = lin_alg.get_sub_matrix(self.pixel_table,
                                                               row - kernel_radius,
                                                               column - kernel_radius,
                                                               size=kernel_size)

                horizontal_strength = img_filter.apply_kernel(pixel_and_surrounding, horizontal_kernel)
                vertical_strength = img_filter.apply_kernel(pixel_and_surrounding, vertical_kernel)

                total_strength = math.sqrt(vertical_strength ** 2 + horizontal_strength ** 2)
                if vertical_strength == 0:
                    edge_orientation = 0
                else:
                    edge_orientation = math.atan(horizontal_strength / vertical_strength)

                self.pixel_table[row][column].new_value = total_strength
                self.pixel_table[row][column].orientation = edge_orientation
                if edge_orientation is None:
                    print(edge_orientation, row, column)

        self.set_new_pixel_values()

    def non_maximum_suppressor(self, kernel_size=5):
        """"""
        "Non maximum suppression."
        kernel_radius = kernel_size // 2
        for row in range(kernel_radius, self.working_image.height - kernel_radius):
            for column in range(kernel_radius, self.working_image.width - kernel_radius):
                pixel_and_surrounding = lin_alg.get_sub_matrix(self.pixel_table,
                                                               row - kernel_radius,
                                                               column - kernel_radius,
                                                               size=kernel_size)

                # Turns off the pixel if it is not the maximum.
                if not img_filter.local_maximum(pixel_and_surrounding, kernel_radius):
                    self.pixel_table[row + kernel_radius][column + kernel_radius].turn_off_pixel()

    def hysteresis_thresholding(self):
        """"""
        lower_threshold = 0.075
        high_threshold = 0.175

    def apply_hough_circle_transform(self):
        """"""
        pass


first_image = "test_images\\real\\nice big crystal.png"

working_image = ImageAnalysis(Image.open(first_image))
working_image.init_greyscale_pixel_table()
working_image.apply_gaussian_blur()


working_image.apply_sobel_edge_detection()

working_image.non_maximum_suppressor()

# for main_row in working_image.pixel_table:
#     for main_pixel in main_row:
#         if main_pixel.orientation is not None:
#             print('value', main_pixel.value, '\norientation', main_pixel.orientation, end=',')
#     print()

