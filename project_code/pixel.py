class GreyPixel:
    """"""

    def __init__(self, pixel_values):
        """Creates an instance of a grey pixel.
        The pixel can hold a """
        self.cache = None
        self.orientation = None

        if isinstance(pixel_values, tuple):
            pixel_values = pixel_values[:3]
            red, green, blue = pixel_values
            pixel_values = int((0.299 * red) + (0.587 * green) + (0.114 * blue))

        self.value = pixel_values

    def __add__(self, other):
        return self.value + other

    def __mul__(self, other):
        return self.value * other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __str__(self):
        angle = self.orientation
        if angle is not None:
            return "{}, {}°".format(self.value, self.orientation)
        return "{}".format(self.value)

    def set_new_value(self):
        self.value = self.cache
        self.cache = None

    def turn_off(self):
        """"""
        self.value = 0
        self.orientation = None

    def is_off(self):
        if self.value == 0 and self.orientation is None:
            return True
        return False

    def is_on(self):
        return not self.is_off()

    def copy_colour_variant(self):
        pixel_value = self.value

        return pixel_value,  pixel_value, pixel_value
