import analyse_image as open_image
from project_code.image_manipulation.classes.wrapper import image_transform as analyse_image
import tkinter as tk
from tkinter import filedialog as file_dialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading as thread


# GuySoft
# https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python/65447493#65447493
class Thread_R(thread.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        thread.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        thread.Thread.join(self)
        return self._return


image_queue = list()

image_queue_thread = thread.Thread()


class ApplicationImageAnalysis(tk.Frame):
    """
    Frame that can contain an active image location.

    The frame can build all frames of the application.
    """

    def __init__(self):
        """Creates an Application Image Analysis object.

        The object consist of a tkinter frame with the capabilities of building the various pages of the applications.
        """
        super().__init__()
        self.queue_locations = []
        self.settings = dict()
        self.current_image = None

        self.build_start_menu()

    def clear_frame(self):
        """Unpacks and destroys all widgets packed to the frame."""
        for widget in self.pack_slaves():
            widget.pack_forget()
            widget.destroy()

    def hough_circle_transform(self):
        """
        Manipulates an images to find circles with Hough Circle Transform.

        Does the following steps separately:
        - convert to greyscale
        - apply gaussian blur
        - apply sobel edge detection
        - canny non-maximum suppressor.
        - canny hysteresis_thresholding.
        - hough transform for small radii (2 - 10)
        lastly prints all found circle centers in the hough transform

        Returns
        -------
        None
            The image has been searched for circles and the found circles have been drawn over the image.
        """
        self.current_image.apply_canny(noise=self.settings['noise'])
        found_circles = self.current_image.apply_hough_circle_transform(self.settings['size'])
        self.build_show_results(found_circles)

    def save_image_settings(self, width, size, noise):
        """Saves the settings to the frame object. Runs the run menu.

        Parameters
        ----------
        width: int
            Real width of the picture.
        size: int
            Approximate size of the pixels.
        noise: int
            Approximate amount of noise in the image.
        Returns
        -------
        None
            The settings have been saved and the user is directed to the run menu.
        """
        width //= self.current_image.working_image.width
        self.settings = {'zoom': width,
                         'size': size,
                         'noise': noise}
        self.build_run_menu()

    def build_start_menu(self):
        """
        Asks user if they want to load in an image.

        Give option to load in Image.
        If an old image is loaded in, give the option to the image analysis menu.
        """
        self.clear_frame()

        information_label = tk.Label(master=self,
                                     text='Automatically counts and measures all round structures.')

        load_file_button = tk.Button(master=self,
                                     text="Load Image",
                                     command=self.load_new_image)
        information_label.pack()
        load_file_button.pack()

        if self.current_image is not None:
            use_old_file = tk.Button(master=self,
                                     text="Use previous image",
                                     command=self.build_run_menu)
            use_old_file.pack()

    def load_new_image(self):
        """
        File dialog with the user.

        If an image is correctly read in, opens the image analysis menu.
        """
        # Source: https://pythonspot.com/tk-file-dialogs/
        image_location = file_dialog.askopenfilename(initialdir="/",
                                                     title="Select file",
                                                     filetypes=(("jpeg files", "*.jpg"),
                                                                ("png files", "*.png"),
                                                                ("tiff files", "*.tiffany"),
                                                                ("all files", "*.*")))

        if image_location != "":
            self.current_image = analyse_image.TransformImage(open_image.open_standard_width(image_location))
            self.image_information_enquiry()

    def image_information_enquiry(self):
        """"""
        self.clear_frame()
        explanation_label = tk.Label(self, text="Please enter the following information:"
                                                "\n\nRate te following measurements from 1 to 5"
                                                "\n1 is small, 5 is big.\nLeave it at 0 if you do not know.")

        width_label = tk.Label(self, text="Total width in µm: ")
        width_box = tk.Entry(self)

        size_circles_label = tk.Label(self,
                                      text="Approximate size of the circles:")
        size_scale = tk.Scale(self,
                              from_=0,
                              to=5,
                              tickinterval=1)

        noise_label = tk.Label(self,
                               text="Noise in the image")

        noise_scale = tk.Scale(self,
                               from_=0,
                               to=5,
                               tickinterval=1)

        save_settings_button = tk.Button(self,
                                         text="Save Settings",
                                         command=lambda: self.save_image_settings(width=int(width_box.get().strip()),
                                                                                  size=size_scale.get(),
                                                                                  noise=noise_scale.get()))

        more_information = tk.Button(self, text="More Information", command=self.build_information_settings)
        cancel_button = tk.Button(self,
                                  text="Cancel",
                                  command=self.build_start_menu)

        explanation_label.pack()
        width_label.pack()
        width_box.pack()

        size_circles_label.pack()
        size_scale.pack()

        noise_label.pack()
        noise_scale.pack()

        save_settings_button.pack()
        more_information.pack()
        cancel_button.pack()

    def build_information_settings(self):
        """"""
        self.clear_frame()
        explanation_size = tk.Label(self, text="The approximate sizes of the circles correspond to:\n"
                                               "circle size    Diameter in percentage length of the image\n"
                                               "0            :     1%   - 20%                            \n"
                                               "1            :     0.6% - 1.5%                           \n"
                                               "2            :     1.5% - 3%                             \n"
                                               "3            :     3%   - 10%                            \n"
                                               "4            :     6%   - 10%                            \n"
                                               "5            :     10%  - 20%                            \n")

        explanation_noise = tk.Label(self, text="The amount of clutter in the picture."
                                                "\n1 is very little and 5 is a lot.")

        settings_button = tk.Button(self, text="Back to Settings", command=self.image_information_enquiry)
        main_menu_button = tk.Button(self, text="Main Menu", command=self.build_start_menu)

        explanation_size.pack()
        explanation_noise.pack()
        settings_button.pack()
        main_menu_button.pack()

    def build_run_menu(self):
        """
        Choice menu for how to analyze the image that is loaded.

        The menu has the following choices:
        - Find edges with canny edge detection.
        - Count circles with hough circle transform.
        - Cancel and load a new image.

        Returns
        -------
        None
            Option Menu is being shown in the frame.
        """
        self.clear_frame()

        count_circles = tk.Button(master=self,
                                  text='Count and measure circles',
                                  command=self.hough_circle_transform)
        settings_button = tk.Button(master=self,
                                    text='Image settings',
                                    command=self.image_information_enquiry)
        cancel_button = tk.Button(master=self,
                                  text='Cancel',
                                  command=self.build_start_menu)

        count_circles.pack()
        settings_button.pack()
        cancel_button.pack()

    def build_show_results(self, results):
        """
        Shows results of the Hough transform.

        Shows the average diameters and amount of counted circles.

        Parameters
        ----------
        results: list [(int, int, int)]
            Circle centers found, specified by radius, x-coordinate, y-coordinate

        Returns
        -------
        None
            Results are shown in the frame
        """
        circle_count, mean_diameter, mean_radius = open_image.process_circle_results(results, self.settings['zoom'])

        total_circle_label = tk.Label(self, text="Total amount of circles: {}".format(circle_count))
        mean_diameter_label = tk.Label(self, text="Average diameter: {:.2f} ".format(mean_diameter))
        mean_radius_label = tk.Label(self, text="Average radius: {:.2f}".format(mean_radius))
        self.current_image.draw_circles(results, (255, 0, 0))

        load_image = tk.Button(self, text="Load Next Image", command=self.load_new_image)

        result_image = self.render_image()
        self.clear_frame()

        total_circle_label.pack()
        mean_diameter_label.pack()
        mean_radius_label.pack()
        result_image.pack()
        load_image.pack()

    def render_image(self, background='white'):
        """"""
        width = self.current_image.working_image.width
        height = self.current_image.working_image.height
        # renders the image
        logo = ImageTk.PhotoImage(self.current_image.working_image)

        # creates a canvas and draws the image in it.
        canvas = tk.Canvas(self, background=background, width=width, height=height, highlightthickness=0)
        canvas.create_image((0, 0), anchor='nw', image=logo)
        canvas.image = logo

        return canvas


if __name__ == "__main__":
    root = tk.Tk()
    a_frame = ApplicationImageAnalysis()
    a_frame.pack()
    root.mainloop()
