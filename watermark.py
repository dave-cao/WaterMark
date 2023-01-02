from PIL import Image, ImageDraw, ImageFont


class WaterMark:
    def __init__(self, background, logo, watermark_text):
        """The watermark class is the object that handles watermarking an image.

        Args:
            background(str): path to a backround image to watermark
            logo(str): path to a logo to put on background
            watermark_text(str): a string of text to put onto background
        """

        self.background = Image.open(background)
        try:
            self.logo = Image.open(logo)
        # No logo provided
        except AttributeError:
            self.logo = ""

        self.background_width, self.background_height = self.background.size
        self.logosize = 175
        self.textsize = 35
        self.text = watermark_text

        # default text colour is WHITE
        self.textcolour = "#FFFFFF"

    def draw_text(self):
        """Draws given text onto bottom right of background"""

        draw = ImageDraw.Draw(self.background)

        font = ImageFont.truetype("./assets/arial.ttf", self.textsize)
        left, top, right, bottom = font.getbbox(self.text)

        textwidth = right - left
        textheight = bottom - top

        # calcualte x, y of text
        margin = 50
        x = self.background_width - textwidth - margin
        y = self.background_height - textheight - margin

        draw.text((x, y), self.text, font=font, fill=self.textcolour)

    def paste_logo(self):
        """Paste the logo on top of background at the top right."""
        self.logowidth, self.logoheight = self.logo.size

        # scale the self.logo to a smaller size
        scale = self.logosize
        new_logowidth = int(self.logowidth / self.logowidth * scale)
        new_logoheight = int(self.logoheight / self.logowidth * scale)
        self.logo = self.logo.resize((new_logowidth, new_logoheight))

        # In case the image logo is not transparent
        # If the logo is not transparent this will give a value error
        try:
            self.background.paste(self.logo, (0, 30), self.logo)
        except ValueError:
            self.background.paste(self.logo, (0, 30))

    def show(self):
        """Gives a preview of the watermark."""
        self.draw_text()
        if self.logo:
            self.paste_logo()
        self.background.show()

    def get_watermark_image(self):
        """Gets the watermarked image

        Returns(image object): the watermarked image
        """
        self.draw_text()
        if self.logo:
            self.paste_logo()
        return self.background

    def set_logosize(self, size):
        """Sets the size of the logo

        Args:
            size(str): the input logo size given by the user
        """
        if size:
            self.logosize = int(size)

    def set_textsize(self, size):
        """Sets the size of the watermarked text

        Args:
            size(str): the input text size given by the user

        """
        if size:
            self.textsize = int(size)

    def set_textcolour(self, chosen_colour):
        """Sets the colour of the text

        Args:
            chosen_colour(str): the chosen colour given by the user

        """
        if chosen_colour == "Black":
            self.textcolour = "#000000"
        elif chosen_colour == "White":
            self.textcolour = "#FFFFFF"
