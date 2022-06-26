class ContinuousEdge:
    """
    An object representing a continuous edge.

    Has a list attribute ``pixels``.

    The edge has the following member functions:
    - Add a pixel to the edge
    - Add all missing pixels to the edge, starting from an x, y coordinate.
    - Turn off all pixels inside the edge.
    - The edge can validate itself, checking if one of its pixels meets a value threshold.
    """
    def __init__(self, start_pixel=None):
        """
        Creates a continuous edge object.

        Adds the first pixel to the attribute ``pixels``.

        Parameters
        ----------
        start_pixel: pixels.GreyPixel
            The first pixel of the edge that was found.

        Returns
        -------
        ContinuousEdge
            The created Continuous Edge object
        """
        self.pixels = list()
        if start_pixel is not None:
            self.add_pixel(start_pixel)

    def add_pixel(self, input_pixel):
        """
        Adds a pixel to the pixel table of the edge.

        Parameters
        ----------
        input_pixel: int
            Pixel to be added to the pixel table.

        Returns
        -------
        None
            Pixel is added to the pixel table
        """
        self.pixels.append(input_pixel)

    def fill_missing_pixels(self, value_table, start_x=0, start_y=0, pixel_range=1):
        """
        Search for all pixels in the edge.

        Searches for turned on pixels adjacent to the starting pixel of the edge. If found, these pixels are added to
        Continuous Edge. That pixel will be chosen to search new adjacent pixels from.
        Continuous searching for adjacent pixels until none are found.

        Parameters
        ----------
        value_table: Pixel Table
            Contains the image with edges.
        start_x: int
            Column index of the starting pixel.
        start_y: int
            Row index of the starting pixel.
        pixel_range: int
            Maximum distance between edge pixels.

        Returns
        -------
        None
            All adjacent pixels have been added
        """
        total_height, total_width = value_table.shape
        current_row = start_y
        current_column = start_x
        active_pixels_around = True

        # Searches until no adjacent turned on pixels are found.
        while active_pixels_around:
            value_table[current_row][current_column].cache = 1
            neighbor_found = False
            for adjacent_row_index in range(current_row - pixel_range,
                                            current_row + pixel_range + 1):
                # Skips the row if it is out of bounds to the image.
                if adjacent_row_index < 0 or adjacent_row_index >= total_height:
                    continue
                for adjacent_column_index in range(current_column - pixel_range,
                                                   current_column + pixel_range + 1):
                    # Skips the column if it is out of bound to the image.
                    if adjacent_column_index < 0 or adjacent_column_index >= total_width:
                        continue

                    adjacent_pixel = value_table[adjacent_row_index][adjacent_column_index]
                    if adjacent_pixel.is_on():
                        # Skips the pixel if it has already been checked.
                        if adjacent_pixel.cache == 1:
                            continue

                        # Adds pixel to the pixel table inside edge.
                        self.add_pixel(adjacent_pixel)
                        # Updates values of last found edge pixel.
                        current_row = adjacent_row_index
                        current_column = adjacent_column_index
                        # Turns on flag to break out of the inner loop and not the outer.
                        neighbor_found = True
                        continue

                # Sets no neighbour flag when no neighbors have been found in the loop.
                if neighbor_found:
                    break

            # Breaks the outer loop when no neighboring pixel was found.
            if not neighbor_found:
                active_pixels_around = False

    def turn_off(self):
        """Turns off all pixels in the ``pixels`` attribute."""
        for pixel in self.pixels:
            pixel.turn_off()

    def validate(self, max_hysteresis):
        """
        Validates if the edge is partly a strong edge. Turns off the edge when it is not.

        For every pixel inside the pixel table, checks if the pixel is stronger than the given threshold. If a strong
        pixel is found, does nothing.
        If no strong pixels are found, all pixels are turned off.

        Parameters
        ----------
        max_hysteresis: int:
            Threshold for strong pixel response.

        Returns
        -------
        None
            The edge has been validated and has been turned off if it failed the validation.
        """
        failed = True
        for current_pixel in self.pixels:
            if current_pixel > max_hysteresis:
                failed = False
                break
        if failed:
            self.turn_off()
