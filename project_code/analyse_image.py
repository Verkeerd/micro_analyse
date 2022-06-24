import image_analysis as analyse

from PIL import Image as pillowImage


def open_standard_width(file_name):
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
    kernel_size = 3
    active_image = open_standard_width(file_name)

    working_image = analyse.ImageAnalysis(active_image)
    working_image.plot_pixel_table()

    working_image.apply_gaussian_blur(kernel_size)
    working_image.plot_pixel_table()

    working_image.apply_sobel_edge_detection()
    working_image.plot_pixel_table()

    working_image.apply_just_canny_edge_detection(kernel_size)
    working_image.plot_pixel_table()


def houghs_with_canny(file_name):
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

    Returns
    -------
    None
    """
    kernel_size = 3

    active_image = open_standard_width(file_name)

    working_image = analyse.ImageAnalysis(active_image)
    working_image.plot_pixel_table()

    working_image.apply_gaussian_blur(kernel_size)
    working_image.plot_pixel_table()

    working_image.apply_sobel_edge_detection()
    working_image.plot_pixel_table()

    working_image.apply_just_canny_edge_detection(kernel_size)
    working_image.plot_pixel_table()

    all_results = list()
    for i in range(90, 111):
        all_results += working_image.apply_hough_circle_transform(i)
    print(all_results)

    working_image.draw_over_image([(x, y) for r, x, y in all_results], (255, 0, 0))
