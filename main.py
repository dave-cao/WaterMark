# A program that will automatically watermark your stuffs

# Using pillow to image image
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageTk

# with Image.open("./shanksOnePiece.png") as image:
#     print(image.format, image.size, image.mode)

# create an image object
class WaterMark:
    def __init__(self, background, logo, watermark_text):

        self.background = Image.open(background)
        try:
            self.logo = Image.open(logo)
        # no logo provided
        except AttributeError:
            self.logo = ""

        self.background_width, self.background_height = self.background.size
        self.logosize = 175
        self.textsize = 35
        self.text = watermark_text
        self.textcolour = "#FFFFFF"

    def draw_text(self):

        draw = ImageDraw.Draw(self.background)

        font = ImageFont.truetype("arial.ttf", self.textsize)
        left, top, right, bottom = font.getbbox(self.text)

        textwidth = right - left
        textheight = bottom - top

        # calcualte x, y of text
        margin = 50
        x = self.background_width - textwidth - margin
        y = self.background_height - textheight - margin

        draw.text((x, y), self.text, font=font, fill=self.textcolour)

    def paste_logo(self):
        # Paste self.logo
        self.logowidth, self.logoheight = self.logo.size

        # scale the self.logo
        scale = self.logosize
        new_logowidth = int(self.logowidth / self.logowidth * scale)
        new_logoheight = int(self.logoheight / self.logowidth * scale)
        self.logo = self.logo.resize((new_logowidth, new_logoheight))

        # In case the image logo is not transparent
        try:
            self.background.paste(self.logo, (0, 30), self.logo)
        except ValueError:
            self.background.paste(self.logo, (0, 30))

    def show(self):
        self.draw_text()
        if self.logo:
            self.paste_logo()
        self.background.show()

    def get_watermark_image(self):
        self.draw_text()
        if self.logo:
            self.paste_logo()
        return self.background

    def set_logosize(self, size):
        if size:
            self.logosize = int(size)

    def set_textsize(self, size):
        if size:
            self.textsize = int(size)

    def set_textcolour(self, chosen_colour):
        if chosen_colour == "Black":
            self.textcolour = "#000000"
        elif chosen_colour == "White":
            self.textcolour = "#FFFFFF"


# ======================================================================== #
# TKINTER FUNCTIONS
def upload_file(window):
    global selected_img
    f_types = [
        ("PNG Files", "*.png"),
        ("Jpg Files", "*.jpg"),
    ]  # type of files to select
    filename = filedialog.askopenfilename(filetypes=f_types)

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
        command=lambda: create_watermark_preview(window, filename),
    )
    image_button.grid(column=1, row=7, columnspan=4)


def create_watermark_preview(window, filename):

    watermark_text = watermark_input.get()
    water = WaterMark(filename, logofilename, watermark_text)
    water.set_textcolour(chosen_colour.get())

    logosize = logosize_input.get()
    textsize = textsize_input.get()
    if logosize:
        try:
            logosize = int(logosize_input.get())
        # If the input is not a valid integer
        except ValueError:
            tk.messagebox.showerror(
                title="Error!", message="That is not a valid logo size!"
            )

    if textsize:
        try:
            textsize = int(textsize_input.get())
        except ValueError:
            tk.messagebox.showerror(
                title="Error", message="That is not a valid text size!"
            )
    water.set_logosize(logosize)
    water.set_textsize(textsize)
    new_img = water.get_watermark_image()
    new_img.show()

    save_button = tk.Button(
        text="Save Image",
        highlightthickness=0,
        command=lambda: save_image(new_img, filename),
    )
    save_button.grid(row=8, column=1, pady=20, columnspan=4)


def save_image(img, filename):
    f, e = os.path.splitext(filename)
    img.save(f"{f}_watermarked{e}")
    save_button = tk.Button(
        text="Save Image", highlightthickness=0, state="disabled", fg="red"
    )
    save_button.grid(row=8, column=1, pady=20, columnspan=3)
    tk.messagebox.showinfo(title="Success!", message="Picture watermarked and saved!")


def upload_logo():
    global logofilename
    f_types = [
        ("PNG Files", "*.png"),
        ("Jpg Files", "*.jpg"),
    ]  # type of files to select
    logofilename = filedialog.askopenfilename(filetypes=f_types)

    show_filename = ""
    for i in range(len(logofilename) - 1, -1, -1):
        char = logofilename[i]
        if char == "/" or char == "\\":
            break
        else:
            show_filename = char + show_filename

    logofile_label.config(text=show_filename)


def batch_upload():
    f_types = [
        ("PNG Files", "*.png"),
        ("Jpg Files", "*.jpg"),
    ]  # type of files to select
    batch_files = filedialog.askopenfilename(multiple=True, filetypes=f_types)

    watermark_text = watermark_input.get()
    if not logofilename and not watermark_text:
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
        # SAME AS CREATE _ WATERMAKR PREVIEW DRY THIS LATER

        water = WaterMark(file, logofilename, watermark_text)
        water.set_textcolour(chosen_colour.get())
        logosize = logosize_input.get()
        textsize = textsize_input.get()
        if logosize:
            try:
                logosize = int(logosize_input.get())
            # If the input is not a valid integer
            except ValueError:
                tk.messagebox.showerror(
                    title="Error!", message="That is not a valid logo size!"
                )

        if textsize:
            try:
                textsize = int(textsize_input.get())
            except ValueError:
                tk.messagebox.showerror(
                    title="Error", message="That is not a valid text size!"
                )
        water.set_logosize(logosize)
        water.set_textsize(textsize)
        new_img = water.get_watermark_image()

        # FKKK
        f, e = os.path.splitext(file)
        show_filename = ""
        for i in range(len(f) - 1, -1, -1):
            char = f[i]
            if char == "/" or char == "\\":
                break
            else:
                show_filename = char + show_filename
        new_img.save(f"{directory}/{show_filename}_watermarked{e}")

    tk.messagebox.showinfo(
        title="Success", message="All pictures watermarked and saved!"
    )


# =================================
# TKINTER UI


import tkinter as tk
from tkinter import filedialog

FONT_NAME = "Courier"
FONT_SIZE = 15

font = FONT_NAME, FONT_SIZE

THEME_COLOR = "#375362"
window = tk.Tk()
window.title("WaterMark")
window.config(padx=20)
window.geometry("700x830")
logofilename = ""

# logo image
canvas = tk.Canvas(width=450, height=300, highlightthickness=0)
water_image = tk.PhotoImage(file="./new.png")
canvas.create_image(250, 150, image=water_image)
canvas.grid(row=0, column=1, columnspan=4)


# Upload logo filename
logofile_label = tk.Label(text="Upload your logo:", font=font, highlightthickness=0)
logofile_label.grid(row=1, column=1)
logofile_button = tk.Button(
    text="Upload", font=font, highlightthickness=0, command=lambda: upload_logo()
)
logofile_button.grid(row=1, column=2)

# WATERMARK TEXT
watermark_label = tk.Label(text="WaterMark text:", font=font, highlightthickness=0)
watermark_label.grid(row=2, column=1)
watermark_input = tk.Entry(width=20, highlightthickness=0)
watermark_input.grid(row=2, column=2, pady=20)

# Ask for WATERMARK color
chosen_colour = tk.StringVar(window)
chosen_colour.set("Select a colour")
options = ["White", "Black"]
watermark_drop = tk.OptionMenu(window, chosen_colour, *options)
watermark_drop.grid(row=2, column=3, padx=10)

# Input for logo and input size
logosize_label = tk.Label(
    text="Logo Size (default=175):", font=(FONT_NAME, FONT_SIZE), highlightthickness=0
)
logosize_label.grid(row=3, column=1)
logosize_input = tk.Entry(width=10, highlightthickness=0)
logosize_input.grid(row=3, column=2)


# Input for text and input size
textsize_label = tk.Label(
    text="Text Size (default=35): ", font=(FONT_NAME, FONT_SIZE), highlightthickness=0
)
textsize_label.grid(row=4, column=1)
textsize_input = tk.Entry(width=10, highlightthickness=0)
textsize_input.grid(row=4, column=2)

# Ask to upload file
title = tk.Label(
    text="Upload your image here", font=(FONT_NAME, FONT_SIZE), highlightthickness=0
)
title.grid(row=5, column=1, columnspan=4, pady=10)


# BATCH WATERMARK
batch_watermark_button = tk.Button(
    text="Batch Upload", font=font, command=lambda: batch_upload(), width=20
)
batch_watermark_button.grid(row=6, column=0, columnspan=2)

# upload button
up_button = tk.Button(
    text="Upload Image",
    highlightthickness=0,
    font=font,
    command=lambda: upload_file(window),
    width=20,
)

up_button.grid(row=6, column=2, pady=20, columnspan=2)

window.mainloop()
