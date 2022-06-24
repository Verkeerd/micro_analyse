import numpy as np
import pixel as pixels
import edge as edges


class PixelTable:
    def __init__(self, width, height):
        self.pixels = np.ndarray((height, width), dtype=pixels.GreyPixel)

    def add_grey_pixels(self, image):
        for row in range(image.height):
            for column in range(image.width):
                pixel_rgb = image.getpixel((column, row))
                pixel_value = pixels.GreyPixel(pixel_rgb)
                self.pixels[row][column] = pixel_value

    def set_new_pixel_values(self):
        """Sets the value of the cache to a pixel for every pixel in the pixel table."""
        for row in self.pixels:
            for active_pixel in row:
                if active_pixel.cache is not None:
                    active_pixel.value = int(active_pixel.cache)
                    active_pixel.cache = None

    def clear_cache(self):
        """Clears the cache of every pixel in the pixel table."""
        for row in self.pixels:
            for active_pixel in row:
                if active_pixel.cache is not None:
                    active_pixel.cache = None

    def turn_off_borders(self, width):
        pass

    def get_luminosity_active_pixels(self):
        """"""
        all_luminosities = list()
        for row_pixels in self.pixels:
            for current_pixel in row_pixels:
                if current_pixel.value != 0:
                    all_luminosities.append(current_pixel.value)

        return all_luminosities

    def find_continuous_edges(self, pixel_range=1):
        """
        Searches for and groups connected pixels which are on.

        Checks for every pixel if the pixel is on, if the pixel is on,
        """
        all_edges = list()
        total_row_length, total_column_length = self.pixels.shape
        for row_index in range(2, total_row_length - 2):
            for column_index in range(2, total_column_length - 2):
                current_pixel = self.pixels[row_index][column_index]
                if current_pixel.is_off():
                    continue
                if current_pixel.cache == 1:
                    continue
                active_edge = edges.ContinuousEdge(current_pixel)
                active_pixels_around = True
                edge_row_index = row_index
                edge_column_index = column_index
                while active_pixels_around:
                    self.pixels[edge_row_index][edge_column_index].cache = 1
                    neighbor_found = False
                    for adjacent_row_index in range(edge_row_index - pixel_range, edge_row_index + pixel_range + 1):
                        if adjacent_row_index < 0 or adjacent_row_index >= self.pixels.shape[0]:
                            continue
                        for adjacent_column_index in range(edge_column_index - pixel_range,
                                                           edge_column_index + pixel_range + 1):
                            if adjacent_column_index < 0 or adjacent_column_index >= self.pixels.shape[1]:
                                continue
                            adjacent_pixel = self.pixels[adjacent_row_index][adjacent_column_index]
                            if adjacent_pixel.cache == 1:
                                continue
                            if adjacent_pixel.is_on():
                                active_edge.add_pixel(adjacent_pixel)
                                edge_row_index = adjacent_row_index
                                edge_column_index = adjacent_column_index
                                neighbor_found = True
                        if neighbor_found:
                            break
                    if not neighbor_found:
                        active_pixels_around = False

                all_edges.append(active_edge)

        self.clear_cache()

        return all_edges

    def rgb_copy(self):
        total_height, total_width = self.pixels.shape
        rgb_table = list()
        for row_index in range(total_height):
            current_pixel_row = list()
            for column_index in range(total_width):
                rgb = self.pixels[row_index][column_index].copy_colour_variant()
                current_pixel_row.append(rgb)
            rgb_table.append(current_pixel_row)

        return np.array(rgb_table)
