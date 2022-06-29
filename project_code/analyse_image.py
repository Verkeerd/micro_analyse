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


def canny_with_images_between_stages(file_name):
    """
    Manipulates an images with canny edge detection and prints images between every step.

    Does the following steps separately and prints an image after each individual step:
    - convert to greyscale
    - apply gaussian blur
    - apply sobel edge detection
    - canny non-maximum suppressor.
    - canny hysteresis_thresholding.

    Parameters
    ----------
    file_name : string
        The name of the location of the image to manipulate.

    Returns
    -------
    None
    """
    kernel_size = 5
    active_image = open_standard_width(file_name)

    working_image = analyse.TransformImage(active_image)
    working_image.plot_pixel_table()

    working_image.apply_gaussian_blur(kernel_size)
    working_image.plot_pixel_table()

    working_image.apply_sobel_edge_detection()
    working_image.plot_pixel_table()

    working_image.apply_canny_edge_detection(kernel_size)
    working_image.plot_pixel_table()

    return working_image


def hough_with_canny(file_name, size):
    """
    Manipulates an images with canny edge detection and prints images between every step.

    Does the following steps separately:
    - convert to greyscale
    - apply gaussian blur
    - apply sobel edge detection
    - canny non-maximum suppressor.
    - canny hysteresis_thresholding.
    - hough transform for small radii (2 - 10)
    lastly prints all found circle centers in the hough transform

    Parameters
    ----------
    file_name : string
        The name of the location of the image to manipulate.
    size: int
        Approximate size of the circles.

    Returns
    -------
    None
        The image has been searched for circles and the found circles have been drawn over the image.
    """
    active_image = open_standard_width(file_name)

    working_image = analyse.TransformImage(active_image)
    # working_image.apply_canny()
    working_image.apply_canny_show_images()
    found_circles = working_image.apply_hough_circle_transform(size)
    return found_circles

    working_image.draw_circles(found_circles, (255, 0, 0))


def process_circle_results(circle_results, zoom_factor):
    """Counts"""
    circle_count = 0
    total_radius = 0

    for radius in circle_results:
        for coordinates in circle_results[radius]:
            circle_count += 1
            total_radius += radius

    if circle_count == 0:
        return 0, 0, 0

    total_radius *= zoom_factor

    mean_diameter = (total_radius * 2) / circle_count

    mean_radius = total_radius / circle_count

    return circle_count, mean_diameter, mean_radius
