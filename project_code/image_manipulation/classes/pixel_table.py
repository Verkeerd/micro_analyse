import numpy as np
from project_code.image_manipulation.classes import \
    edge as edges, \
    pixel as pixel


class PixelTable:
    """
    A pixel table containing pixels representing an image.

    Has the attribute ``pixels``, which is an array that contains the pixels.
    The pixels have to be Grey Pixels.

    Contains member functions that can manipulate the pixel table:
    - Function to automatically itself with the greyscale variant of an image.
    - Set pixel cache to new value.
    - Clear pixel cache.
    - Compose list of luminosity of active pixels.
    - Find continuous edges inside the pixel table.
    - Compose a rbg copy of the pixel table.
    """
    def __init__(self, width, height):
        """
        Creates a Pixel Table object.

        Parameters
        ----------
        width: int
            total width of the pixel table.
        height: int
            total height of the pixel table.

        Returns
        -------
        PixelTable
            The created Pixel Table object.
        """
        self.pixels = np.ndarray((height, width), dtype=pixel.GrayPixel)

    def fill_with_image(self, image):
        """
        Fills the Pixel Table with an image.

        Sets the attribute ``pixels`` to Grey Pixel variants of the images pixels.

        Parameters
        ----------
        image: pillow.Image
            The image to convert to greyscale and store into the pixel table.

        Returns
        -------
        None
            The pixel table is filled with the greyscale variant of the image.
        """
        for row in range(image.height):
            for column in range(image.width):
                pixel_rgb = image.getpixel((column, row))
                pixel_value = pixel.GrayPixel(pixel_rgb)
                self.pixels[row][column] = pixel_value

    def set_new_pixel_values(self):
        """Sets the value of the cache to a pixel for every pixel in the pixel table."""
        for row in self.pixels:
            for active_pixel in row:
                active_pixel.set_new_value()

    def clear_cache(self):
        """Clears the cache of every pixel in the pixel table."""
        for row in self.pixels:
            for active_pixel in row:
                active_pixel.cache = None

    def turn_off_borders(self, border_width=2):
        """
        Turns off the borderpixels inside the pixel table.
        """
        total_height, total_width = self.pixels.shape
        for row_index in range(border_width):
            for column_index in range(total_width):
                self.pixels[row_index, column_index].turn_off()
                self.pixels[-row_index, column_index].turn_off()

        for row_index in range(border_width, total_height - border_width):
            for column_index in range(border_width):
                self.pixels[row_index][column_index].turn_off()
                self.pixels[row_index][-column_index].turn_off()

    def get_active_pixels(self):
        """Gets a list with all pixels inside the table that are turned on."""
        active = list()
        for row_pixels in self.pixels:
            for current_pixel in row_pixels:
                if current_pixel.is_off():
                    active.append(current_pixel)
        return active

    def get_luminosity_active_pixels(self):
        """Composes a list of pixel values of all pixels that are turned on."""
        return [active_pixel.value for active_pixel in self.get_active_pixels()]

    def find_continuous_edges(self):
        """
        Searches for and groups connected pixels which are on.

        Checks for every pixel if the pixel is on. If the pixel is on, nearby pixels are searches for other pixels that
        are turned on to add to the edge. If no pixels are found, the edge is completed.

        Returns
        -------
        list: [ContinuousEdge]
            A list with all found Continuous Edges.
        """
        all_edges = list()
        table_height, table_width = self.pixels.shape
        for row_index in range(2, table_height - 2):
            for column_index in range(2, table_width - 2):
                current_pixel = self.pixels[row_index][column_index]
                # skips the pixel if it is off.
                if current_pixel.is_off():
                    continue
                # skips the pixel if it has already been used in a different edge.
                if current_pixel.cache == 1:
                    continue
                active_edge = edges.ContinuousEdge(current_pixel)
                active_edge.fill_missing_pixels(self.pixels, column_index, row_index)
                all_edges.append(active_edge)

        self.clear_cache()

        return all_edges

    def rgb_copy(self):
        """
        Creates a numpy array containing rgb copies of the pixels.

        The rgb will contain the grey value of the pixel.
        """
        total_height, total_width = self.pixels.shape
        rgb_table = list()
        for row_index in range(total_height):
            current_pixel_row = list()
            for column_index in range(total_width):
                rgb = self.pixels[row_index][column_index].copy_colour_variant()
                current_pixel_row.append(rgb)
            rgb_table.append(current_pixel_row)

        return np.array(rgb_table)

    def orientation_copy(self):
        """
        Creates a list with a copy of all pixels based on their orientation.

        All orientations are given a different colour. Pixels without an orientation
        are given the colour black.
        """
        total_height, total_width = self.pixels.shape
        rgb_table = list()

        for row_index in range(total_height):
            current_pixel_row = list()
            for column_index in range(total_width):
                rgb = self.pixels[row_index][column_index].copy_orientation_as_colour()
                current_pixel_row.append(rgb)
            rgb_table.append(current_pixel_row)

        return np.array(rgb_table)
