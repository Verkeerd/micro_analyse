from project_code.image_manipulation import \
    standard_filters as apply_filter, \
    sobel_edge_detector as sobel, \
    canny_edge_detector as canny
import shapes
import pixel_table

import matplotlib.pyplot as plot


class ImageAnalysis(object):
    """"""

    def __init__(self, img):
        self.working_image = img
        image_pixel_table = pixel_table.PixelTable(self.working_image.width, self.working_image.height)
        image_pixel_table.add_grey_pixels(self.working_image)
        self.pixel_values = image_pixel_table

    def method1(self):
        """"""
        return self.working_image.method1()

    def apply_gaussian_blur(self, kernel_size=5):
        """"""
        print('Gauss.')
        apply_filter.gauss_blur(self.pixel_values, kernel_size)

    def apply_sobel_edge_detection(self):
        """"""
        print('Sobel.')
        sobel.run_sobel_edge_detection(self.pixel_values)

    def apply_just_canny_edge_detection(self, kernel_size=5):
        canny.canny_detector(self.pixel_values, kernel_size)

    def apply_canny(self, kernel_size=3):
        self.apply_gaussian_blur(kernel_size)
        self.apply_sobel_edge_detection()
        self.apply_just_canny_edge_detection(kernel_size)

    def find_circles(self, size='mid'):
        """"""
        if size == 'mid':
            radii = range(10, 51, 4)
        elif size == 'small':
            radii = range(2, 11)
        elif size == 'big':
            radii = range(50, 101, 5)
        elif size == 'very_big':
            radii = range(100, 201, 10)

        all_circles = list()
        for radius in radii:
            new_circles = self.apply_hough_circle_transform(radius)
            all_circles += new_circles
        return all_circles

    def apply_hough_circle_transform(self, radius):
        """"""
        print('Hough {}'.format(radius))

        base_circle = shapes.Circle(radius, 0, 0)
        indexes = base_circle.draw()
        accumulator = 1

        image_values = self.pixel_values.pixels

        for row_index in range(radius, image_values.shape[0] - radius):
            for column_index in range(radius, image_values.shape[1] - radius):
                current_pixel = image_values[row_index][column_index]
                if current_pixel.is_off():
                    continue
                for x_shift, y_shift in indexes:
                    perimeter_pixel = image_values[row_index + x_shift][column_index + y_shift]
                    if perimeter_pixel.cache is None:
                        perimeter_pixel.cache = accumulator
                    else:
                        perimeter_pixel.cache += accumulator

        found_circle_centers = list()
        threshold = (0.6 * len(indexes)) // 1

        for row_index in range(radius, image_values.shape[0] - radius):
            for column_index in range(radius, image_values.shape[1] - radius):
                current_pixel = image_values[row_index][column_index]
                if current_pixel.cache is None:
                    continue
                if current_pixel.cache > threshold:
                    # saves the circle center as (radius, x, y)
                    found_circle_centers.append((radius, column_index, row_index))

        self.pixel_values.clear_cache()

        return found_circle_centers

    def plot_pixel_table(self, cut_edge=2):
        """"""
        dpi = 80
        height = self.working_image.height // dpi
        width = self.working_image.width // dpi

        plot.figure(num=None, figsize=(width, height), dpi=dpi, facecolor='w', edgecolor='k')
        image = self.pixel_values.rgb_copy()

        plot.imshow(image)
        plot.show()

    def draw_over_image(self, indexes_to_change, colour, radius=3):
        for x, y in indexes_to_change:
            start_x = x - radius
            end_x = x + radius
            if start_x < 0:
                start_x = 0
            if end_x > self.working_image.width:
                end_x = self.working_image.width
            start_y = y - radius
            end_y = y + radius
            if start_y < 0:
                start_y = 0
            if end_y > self.working_image.width:
                end_y = self.working_image.width
            for draw_x in range(start_x, end_x):
                for draw_y in range(start_y, end_y):
                    self.working_image.putpixel((draw_x, draw_y), colour)
        self.working_image.show()
