angle_colour_dict = {-1.75:    (255,   0,      0),
                     -1.25:    (255,   255,    0),
                     -0.75:    (0,     255,    0),
                     -0.25:    (0,     255,    255),
                     0.25:     (0,     0,      255),
                     0.75:     (255,   0,      255),
                     1.25:     (255,   255,    255),
                     1.75:     (100,   100,    100)}


class GrayPixel:
    """
    An object representing a grey value pixel inside a digital rendition of an image.

    The pixel contains a value, cache and orientation attribute.
    """

    def __init__(self, pixel_values):
        """
        Creates an instance of a Gray Pixel.

        The pixel holds a value between 0 and 255, representing a value in the reality.
        255 is white and 0 is black. The pixel can hold an orientation and a cache.
        If the pixel values are given in rbg, the greyscale is calculated and recorded.

        Parameters
        ----------
        pixel_values
            The values associated with the pixel.

        Returns
        -------
        GrayPixel
            The created Gray Pixel object.
        """
        # Cache and orientation are created for later functionality.
        self.cache = None
        self.orientation = None

        self.value = 0

        # If the pixel value is expressed in rbg, grey value is calculated.
        if isinstance(pixel_values, tuple):
            pixel_values = pixel_values[:3]
            red, green, blue = pixel_values
            pixel_values = int((0.299 * red) + (0.587 * green) + (0.114 * blue))

        self.value = pixel_values

    def __add__(self, other):
        """The sum of the value attribute and other."""
        return self.value + other.value

    def __mul__(self, other):
        """The product of the value attribute and other."""
        return self.value * other.value

    def __eq__(self, other):
        """The value attribute is equal to the other."""
        return self.value == other

    def __ne__(self, other):
        """The value attribute is not equal to the other."""
        return self.value != other

    def __lt__(self, other):
        """The value attribute is less than the other."""
        return self.value < other

    def __gt__(self, other):
        """The value attribute is bigger than the other."""
        return self.value > other

    def __str__(self):
        """Prints a pixel as string by printing its value and, if available, its orientation."""
        angle = self.orientation
        if angle is not None:
            return "{}, {}°".format(self.value, self.orientation)
        return "{}".format(self.value)

    def set_new_value(self):
        """Sets the new value contained in the cache."""
        if self.cache is not None:
            self.value = self.cache
            self.cache = None

    def turn_off(self):
        """Turns the pixel off by resetting its value and orientation."""
        self.value = 0
        self.orientation = None

    def is_off(self):
        """Checks if the pixel is off."""
        if self.value == 0 and self.orientation is None:
            return True
        return False

    def is_on(self):
        """Checks if the pixel is on."""
        return not self.is_off()

    def copy_colour_variant(self):
        """Copies the value as a rgb tuple."""
        pixel_value = int(self.value)
        return pixel_value, pixel_value, pixel_value

    def copy_orientation_as_colour(self):
        """Copies the orientation as rbg colour according to the angle colour dict."""
        if self.orientation is None:
            return 0, 0, 0

        for key in angle_colour_dict:
            if self.orientation <= key:
                return angle_colour_dict[key]

        return 255, 0, 0
