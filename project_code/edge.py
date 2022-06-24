class ContinuousEdge:
    def __init__(self, start_pixel):
        self.pixel_table = [start_pixel]

    def add_pixel(self, input_pixel):
        """Adds a pixel to the pixel table."""
        self.pixel_table.append(input_pixel)

    def turn_off(self):
        """Turns off all pixels in the pixel table."""
        for pixel in self.pixel_table:
            pixel.turn_off()

    def validate(self, max_hysteresis):
        """"""
        failed = True
        for current_pixel in self.pixel_table:
            if current_pixel > max_hysteresis:
                failed = False
                break
        if failed:
            self.turn_off()
