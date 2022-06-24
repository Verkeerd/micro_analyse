import image_analysis as analise
import tkinter as tk
from tkinter import filedialog as file_dialog


def get_image_location(master):
    """
    Creates
    Parameters
    ----------
    master:
        The root object of the tkinter instance.
    Returns
    -------
    string:
        the location path to the image.
    """


class SmallWindow(tk.Frame):
    def __init__(self):
        super().__init__()
        self.image_location = None
        self.queue_locations = []
        self.loading_dialog()

    def clear_frame(self):
        for widget in self.pack_slaves():
            widget.pack_forget()
            widget.destroy()

    def run_canny(self):
        analise.canny_with_images_between_stages(self.image_location)

    def hough_circle_transform(self):
        analise.houghs_with_canny(self.image_location)

    def loading_dialog(self):
        self.clear_frame()
        a_label = tk.Label(master=self, text='Automatically counts and measures all round structures.')
        a_label.pack()
        file_button = tk.Button(master=self, text="Load Image", command=self.load_new_image)
        file_button.pack()

    def load_new_image(self):
        # Source: https://pythonspot.com/tk-file-dialogs/
        self.image_location = file_dialog.askopenfilename(initialdir="/",
                                                          title="Select file",
                                                          filetypes=(("jpeg files", "*.jpg"),
                                                                     ("png files", "*.png"),
                                                                     ("all files", "*.*")))
        self.menu_new_image()

    def menu_new_image(self):
        self.clear_frame()
        canny_button = tk.Button(master=self,
                                 text='Canny',
                                 command=self.run_canny)
        count_circles = tk.Button(master=self,
                                  text='Count and measure circles',
                                  command=self.hough_circle_transform)
        cancel_button = tk.Button(master=self,
                                  text='Cancel',
                                  command=self.loading_dialog)
        canny_button.pack()
        count_circles.pack()
        cancel_button.pack()


root = tk.Tk()
a_frame = SmallWindow()
a_frame.pack()
root.mainloop()
