# A program that will automatically watermark your stuffs

# Using pillow to image image
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageTk

# with Image.open("./shanksOnePiece.png") as image:
#     print(image.format, image.size, image.mode)

# create an image object
class WaterMark:
    def __init__(self, background, logo):

        self.background = Image.open(background)
        self.logo = Image.open(logo)

        self.background_width, self.background_height = self.background.size

    def draw_text(self):

        draw = ImageDraw.Draw(self.background)
        text = "https://davidcao.xyz"

        font = ImageFont.truetype("arial.ttf", 35)
        left, top, right, bottom = font.getbbox(text)

        textwidth = right - left
        textheight = bottom - top

        # calcualte x, y of text
        margin = 50
        x = self.background_width - textwidth - margin
        y = self.background_height - textheight - margin

        draw.text((x, y), text, font=font)

    def paste_logo(self):
        # Paste self.logo
        self.logowidth, self.logoheight = self.logo.size

        # scale the self.logo
        scale = 175
        new_logowidth = int(self.logowidth / self.logowidth * scale)
        new_logoheight = int(self.logoheight / self.logowidth * scale)
        self.logo = self.logo.resize((new_logowidth, new_logoheight))

        self.background.paste(self.logo, (0, 30), self.logo)

    def show(self):
        self.draw_text()
        self.paste_logo()
        self.background.show()

    def get_watermark_image(self):
        self.draw_text()
        self.paste_logo()
        return self.background


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
    image_button.grid(column=1, row=3)


def create_watermark_preview(window, filename):
    water = WaterMark(filename, "./cowlogo.png")
    new_img = water.get_watermark_image()
    new_img.show()

    save_button = tk.Button(
        text="Save Image",
        highlightthickness=0,
        command=lambda: save_image(new_img, filename),
    )
    save_button.grid(column=1, row=4, pady=20)


def save_image(img, filename):
    f, e = os.path.splitext(filename)
    img.save(f"{f}_watermarked{e}")
    save_button = tk.Button(
        text="Save Image", highlightthickness=0, state="disabled", fg="red"
    )
    save_button.grid(column=1, row=4, pady=20)
    tk.messagebox.showinfo(title="Success!", message="Picture watermarked and saved!")


# =================================
# TKINTER UI


import tkinter as tk
from tkinter import filedialog

FONT_NAME = "Courier"
FONT_SIZE = 15

THEME_COLOR = "#375362"
window = tk.Tk()
window.title("WaterMark")
window.geometry("500x630")

# logo image
canvas = tk.Canvas(width=500, height=300, highlightthickness=0)
water_image = tk.PhotoImage(file="./new.png")
canvas.create_image(250, 150, image=water_image)
canvas.grid(column=1, row=0)

# Ask to upload file
title = tk.Label(
    text="Upload your file here", font=(FONT_NAME, FONT_SIZE), highlightthickness=0
)
title.grid(column=1, row=1)

# upload button
up_button = tk.Button(
    text="Upload File",
    highlightthickness=0,
    command=lambda: upload_file(window),
)

up_button.grid(column=1, row=2, pady=20)

window.mainloop()
