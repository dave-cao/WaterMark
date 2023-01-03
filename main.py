"""
This program is meant to watermark your images with a GUI.

Caveats:
    - Logo goes on the top left and text goes on the bottom right. You can fork the
        code and change this however!
    - Only two text colours available at the moment, "White" and "Black"

"""
import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from watermark import WaterMark


def main():
    ui = UI()
    ui.init()


class UI:
    def __init__(self):

        self.FONT_NAME = "Courier"
        self.FONT_SIZE = 15
        self.font = self.FONT_NAME, self.FONT_SIZE

        self.THEME_COLOR = "#375362"
        self.window = tk.Tk()
        self.window.title("WaterMark")
        self.window.config(padx=20)
        self.window.geometry("700x830")
        self.logofilename = ""
        self.f_types = [
            ("PNG Files", "*.png"),
            ("Jpg Files", "*.jpg"),
        ]  # type of files to select

    def init(self):
        self.logo_image()
        self.logo_fileupload()
        self.text()
        self.input_sizes()
        self.upload_title()
        self.upload_images()
        self.window.mainloop()

    def logo_image(self):
        row = 0
        canvas = tk.Canvas(width=450, height=300, highlightthickness=0)

        # prevent image garbage collected
        self.window.one = one = water_image = tk.PhotoImage(
            file="./assets/watermarklogo.png"
        )
        canvas.create_image(250, 150, image=water_image)
        canvas.grid(row=row, column=1, columnspan=4)

    def logo_fileupload(self):
        row = 1

        # Upload logo filename
        self.logofile_label = tk.Label(
            text="Upload your logo:", font=self.font, highlightthickness=0
        )
        self.logofile_label.grid(row=row, column=1)
        logofile_button = tk.Button(
            text="Upload",
            font=self.font,
            highlightthickness=0,
            command=lambda: self.upload_logo(),
        )
        logofile_button.grid(row=row, column=2)

    def text(self):

        row = 2
        # WATERMARK TEXT
        watermark_label = tk.Label(
            text="WaterMark text:", font=self.font, highlightthickness=0
        )
        watermark_label.grid(row=row, column=1)
        self.watermark_input = tk.Entry(width=20, highlightthickness=0)
        self.watermark_input.grid(row=row, column=2, pady=20)

        # Ask for WATERMARK color
        self.chosen_colour = tk.StringVar(self.window)
        self.chosen_colour.set("Select a colour")
        options = ["White", "Black"]
        watermark_drop = tk.OptionMenu(self.window, self.chosen_colour, *options)
        watermark_drop.grid(row=row, column=3, padx=10)

    def input_sizes(self):

        logo_inputsize_row = 3
        text_inputsize_row = 4
        # Input for logo and input size
        logosize_label = tk.Label(
            text="Logo Size (default=175):",
            font=self.font,
            highlightthickness=0,
        )
        logosize_label.grid(row=logo_inputsize_row, column=1)
        self.logosize_input = tk.Entry(width=10, highlightthickness=0)
        self.logosize_input.grid(row=logo_inputsize_row, column=2)

        # Input for text and input size
        textsize_label = tk.Label(
            text="Text Size (default=35): ",
            font=self.font,
            highlightthickness=0,
        )
        textsize_label.grid(row=text_inputsize_row, column=1)
        self.textsize_input = tk.Entry(width=10, highlightthickness=0)
        self.textsize_input.grid(row=text_inputsize_row, column=2)

    def upload_title(self):

        row = 5
        # Ask to upload file
        title = tk.Label(
            text="Upload your image here",
            font=self.font,
            highlightthickness=0,
        )
        title.grid(row=row, column=1, columnspan=4, pady=10)

    def upload_images(self):

        row = 6

        # BATCH WATERMARK
        batch_watermark_button = tk.Button(
            text="Batch Upload",
            font=self.font,
            command=lambda: self.batch_upload(),
            width=20,
        )
        batch_watermark_button.grid(row=row, column=0, columnspan=2)

        # upload button
        up_button = tk.Button(
            text="Upload Image",
            highlightthickness=0,
            font=self.font,
            command=lambda: self.upload_file(self.window),
            width=20,
        )

        up_button.grid(row=row, column=2, pady=20, columnspan=2)

    def upload_logo(self):
        self.logofilename = filedialog.askopenfilename(filetypes=self.f_types)
        show_filename = self.get_pwd_filename(self.logofilename)
        self.logofile_label.config(text=show_filename)

    # TKINTER FUNCTION ==================================

    def get_pwd_filename(self, full_path):
        show_filename = ""
        for i in range(len(full_path) - 1, -1, -1):
            char = full_path[i]
            if char == "/" or char == "\\":
                break
            else:
                show_filename = char + show_filename

        return show_filename

    def get_updated_watermark(self, filename):

        watermark_text = self.watermark_input.get()
        water = WaterMark(filename, self.logofilename, watermark_text)
        water.set_textcolour(self.chosen_colour.get())

        logosize = self.logosize_input.get()
        textsize = self.textsize_input.get()

        # Check if logosize or textsize are valid integers
        if logosize:
            try:
                logosize = int(self.logosize_input.get())
            except ValueError:
                tk.messagebox.showerror(
                    title="Error!", message="That is not a valid logo size!"
                )
                return

        if textsize:
            try:
                textsize = int(self.textsize_input.get())
            except ValueError:
                tk.messagebox.showerror(
                    title="Error", message="That is not a valid text size!"
                )
                return

        # Set the sizes in the watermark
        water.set_logosize(logosize)
        water.set_textsize(textsize)

        new_img = water.get_watermark_image()
        return new_img

    def create_watermark_preview(self, filename):

        # get the watermarked image and preview
        new_img = self.get_updated_watermark(filename)
        new_img.show()

        # create a save button to save it
        save_button = tk.Button(
            text="Save Image",
            highlightthickness=0,
            command=lambda: self.save_image(new_img, filename),
        )
        save_button.grid(row=8, column=1, pady=20, columnspan=4)

    def batch_upload(self):
        batch_files = filedialog.askopenfilename(multiple=True, filetypes=self.f_types)

        watermark_text = self.watermark_input.get()
        if not self.logofilename and not watermark_text:
            tk.messagebox.showerror(
                title="Error",
                message="There is no logo or watermark text! If you batch then nothing will change!",
            )
            return

        # Make a directory if it doesn't exist
        directory = "./watermark"
        if not os.path.exists(directory):
            os.mkdir(directory)
        else:
            print("path exists")

        for file in batch_files:
            new_img = self.get_updated_watermark(file)

            # Get file name and make new file inside watermark directory
            f, e = os.path.splitext(file)
            show_filename = self.get_pwd_filename(f)
            new_img.save(f"{directory}/{show_filename}_watermarked{e}")

        tk.messagebox.showinfo(
            title="Success", message="All pictures watermarked and saved!"
        )

    def upload_file(self, window):
        global selected_img
        filename = filedialog.askopenfilename(filetypes=self.f_types)

        selected_img = Image.open(filename)
        width, height = selected_img.size
        scale = 300
        width_new = int(width / width * scale)
        height_new = int(height / width * scale)

        resize_img = selected_img.resize((width_new, height_new))
        selected_img = ImageTk.PhotoImage(resize_img)
        image_button = tk.Button(
            window,
            image=selected_img,
            command=lambda: self.create_watermark_preview(filename),
        )
        image_button.grid(column=1, row=7, columnspan=4)

    def save_image(self, img, filename):
        f, e = os.path.splitext(filename)
        img.save(f"{f}_watermarked{e}")
        save_button = tk.Button(
            text="Save Image", highlightthickness=0, state="disabled", fg="red"
        )
        save_button.grid(row=8, column=1, pady=20, columnspan=3)
        tk.messagebox.showinfo(
            title="Success!", message="Picture watermarked and saved!"
        )


main()
