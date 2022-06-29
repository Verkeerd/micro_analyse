from project_code.image_manipulation.classes.wrapper import image_transform as analyse

from PIL import Image as pillowImage


def open_standard_width(file_name):
    """
    Opens an image with pillow and resizes the image.

    The image is resized to be max 1000 pixels in width and height without altering proportions.

    Parameters
    ----------
    file_name : str
        The path to the image location.

    Returns
    -------
    pillow.Image
        The opened and resized image.
    """
    active_image = pillowImage.open(file_name)
    if active_image.height > active_image.width:
        new_size = (int(1000 / active_image.height * active_image.width), 1000)
    else:
        new_size = (1000, int(1000 / active_image.width * active_image.height))
    return active_image.resize(new_size)


if __name__ == "__main__":
    first_image = "..\\test_images\\digital\\synthetic circles.png"
    second_image = "..\\test_images\\real\\y2 (1.02x) Best Fit.png"
    third_image = "..\\test_images\\real\\y2 (6.94x) regular Fit dark.png"
    fourth_image = "..\\test_images\\real\\y2 (4.4x) regular Fit crowded area.png"
    fifth_image = "..\\test_images\\real\\y2 (6.94x) regular Fit.png"
    sixth_image = "..\\test_images\\real\\Snap-928.jpg"
    seventh_image = "..\\test_images\\real\\S4-bottom-75um-0001.png"
    eighth_image = "..\\test_images\\real\\y2 (4.4x) regular Fit.png"
    ninth_image = "..\\test_images\\digital\\synthetic circles colored in.png"
    tenth_image = "..\\test_images\\online\\img.png"
    open_image = open_standard_width(tenth_image)
    working_image = analyse.TransformImage(open_image)
    working_image.apply_canny_show_images()
    found_circles = working_image.find_circles(3)
    working_image.draw_circles(found_circles, (255, 0, 0))
    working_image.working_image.show()
