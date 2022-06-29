from project_code.image_manipulation import \
    standard_filters as apply_filter, \
    sobel_edge_detector as sobel, \
    canny_edge_detector as canny, \
    hough_circle_transform as hough

from project_code.image_manipulation.classes import \
    pixel_table as tables, \
    basic_shapes as shapes

import matplotlib.pyplot as plot


class TransformImage(object):
    """
    A wrapper around a pillow Image object.

    This wrapper contains functions that perform several transformations. Retains the original image and performs the
    transformations in a greyscale pixel table.

    Transformations available:
    - Gaussian Filter.
    - Sobel Edge Detection
    - Canny Edge Detection
    - Hough Circle Transform

    Other functions:
    - Plots greyscale pixel table in matplotlib.
    - Draws pixel_table over the original image.
    """
    def __init__(self, img):
        """Creates an Image Analysis object.

        Creates a pixel table and fills it with a grey version of pixels of the given image.
        Saves the image inside the object.

        Parameters
        ----------
        img: pillow.Image
            an instance of pillow.Image.

        Returns
        -------
        TransformImage
            The created Image Analysis object.
        """
        self.working_image = img
        image_pixel_table = tables.PixelTable(self.working_image.width, self.working_image.height)
        image_pixel_table.fill_with_image(self.working_image)
        self.pixel_values = image_pixel_table

    def method1(self):
        """Source: """
        return self.working_image.method1()

    def apply_gaussian_blur(self, kernel_size=3):
        """
        Blurs the image using a gaussian blur.

        The image stored inside the Pixel Table is blurred by the kernel.

        Parameters
        ----------
        kernel_size: int
            Size of the gaussian kernel.

        Returns
        -------
        None
            Pixel table image has been blurred.
        """
        apply_filter.gauss_blur(self.pixel_values, kernel_size)

    def apply_sobel_edge_detection(self):
        """
        Searches the image for edges using Sobel Edge Detection.

        The image stored inside the Pixel Table is scanned by the Sobel Edge Detector.

        Returns
        -------
        None
            Pixel table contains the result of the sobel edge detector.
        """
        sobel.run_sobel_edge_detection(self.pixel_values)

    def apply_canny_edge_detection(self, kernel_size=3, noise=2):
        """
        Searches for the strongest edges using Canny Edge Detection.

        Parameters
        ----------
        kernel_size: int
            Diameter of the non-maximum edge intersection; (Double the) length between adjacent pixels with creating
            edges with hysteresis thresholding.
        noise: int
            Approximate amount of noise in the image.

        Returns
        -------
        None
            Pixel table contains the result of the sobel edge detector.
        """
        canny.canny_detector(self.pixel_values, kernel_size, noise)

    def apply_hough_circle_transform(self, size):
        """
        Searches for a circles using Hough Circle Transform.

        Parameters
        ----------
        size: int
            approximate range of radii in the pixels.

        Returns
        -------
        dict: {int: [(int, int)]}
            A dictionary with radii, containing a list with their found circle centers as (x, y).
        """
        return hough.find_circles_unset_size(self.pixel_values, size)

    def apply_canny(self, kernel_size=3, noise=2):
        """
        Searches for edges using Canny Edge Detection.

        Parameters
        ----------
        kernel_size: int
            Amount of steps between adjacent pixels.
        noise: int
            Approximate amount of noise in the image.
        """
        self.apply_gaussian_blur(kernel_size)
        self.apply_sobel_edge_detection()
        self.apply_canny_edge_detection(kernel_size, noise)

    def apply_canny_show_images(self, kernel_size=3):
        """"""
        self.apply_gaussian_blur(kernel_size)
        self.plot_pixel_table(cut_edge=2)

        self.apply_sobel_edge_detection()
        self.plot_pixel_table(cut_edge=2)

        canny.non_maximum_suppressor(self.pixel_values, kernel_size)
        self.plot_pixel_table(cut_edge=2)

        canny.hysteresis_thresholding(self.pixel_values, kernel_size)
        self.plot_pixel_table(cut_edge=2)

    def find_circles(self, size=1):
        """
        Searches for a circles using Hough Circle Transform.

        Searches for a circles inside a specified range.

        Parameters
        ----------
        size: int
            The range of radii.
        """
        return hough.find_circles_unset_size(self.pixel_values, size)

    def plot_pixel_table(self, cut_edge=2):
        """
        Plots the image in the pixel table.

        Parameters
        ----------
        cut_edge: int
            The amount of pixels to cut off of the edges.

        Returns
        -------
        Nothing
            The image is plotted and the plot has been opened.
        """
        dpi = 80
        height = (self.working_image.height // dpi) - cut_edge * 2
        width = (self.working_image.width // dpi) - cut_edge * 2

        plot.figure(num=None, figsize=(width, height), dpi=dpi, facecolor='w', edgecolor='k')
        image = self.pixel_values.rgb_copy()

        plot.imshow(image)
        plot.show()

    def draw_over_image(self, indexes_to_change, colour, radius=3, show=True):
        """
        Draws several points on the Image.

        Draws one or several points on the image for every given index. The image itself, not the rendition inside the
        pixel able, is changed.

        Parameters
        ----------
        indexes_to_change: list [(int, int)]
            Indexes of the pixels whose value to change.
        colour: tuple (int, int, int)
            The colour to draw in as RGB value.
        radius: int
            The pixel radius around the pixel to also draw in.
        show: bool
            Show the image if True. Standard set to True.

        Returns
        -------
        None
            Points are drawn on the image.
        """
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
                    try:
                        self.working_image.putpixel((draw_x, draw_y), colour)
                    except IndexError:
                        continue

        if show:
            self.working_image.show()

    def draw_circles(self, radius_and_indexes, colour, width=1):
        """
        Draws a circle on the image.

        Draws one or several circles on the image for every given index. The image itself, not the rendition inside the
        pixel table, is changed.

        Parameters
        ----------
        radius_and_indexes: tuple (int, int, int)
            Radius, column index (x), row index (y) of the circle
        colour: tuple (int, int, int)
            The colour to draw in as RGB value.
        width: int
            The pixel radius around the pixel to also draw in.

        Returns
        -------
        None
            Circles are drawn on the image.
        """
        for radius in radius_and_indexes:
            base_circle = shapes.Circle(radius, 0, 0)
            base_circle_indexes = base_circle.circumference_indexes()

            for x_index, y_index in radius_and_indexes[radius]:
                self.draw_over_image([(x_index, y_index)], colour, width, False)
                current_indexes = [(base_x + x_index, base_y + y_index) for base_x, base_y in base_circle_indexes]
                self.draw_over_image(current_indexes, colour, width, False)

        self.working_image.show()
