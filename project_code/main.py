import image_analysis as analise
from PIL import Image as pillowImage

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

    analise.houghs_with_canny(ninth_image)

