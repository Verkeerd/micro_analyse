class GreyPixel:
    """"""

    def __init__(self, pixel_values):
        self.new_value = None
        self.orientation = None
        red, green, blue = pixel_values

        perceived_value = (0.299 * red) + (0.587 * green) + (0.114 * blue)
        self.value = perceived_value

    def __add__(self, other):
        return self.value + other

    def __mul__(self, other):
        return self.value * other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def turn_off_pixel(self):
        """"""
        self.value = 0
        self.orientation = None


a_pixel = GreyPixel((8, 2, 3))

a_pixel.turn_off_pixel()

print(a_pixel.value, a_pixel.orientation)
