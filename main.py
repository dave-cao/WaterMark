# A program that will automatically watermark your stuffs

# Using pillow to image image
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# with Image.open("./shanksOnePiece.png") as image:
#     print(image.format, image.size, image.mode)


def to_JPEG():
    for infile in sys.argv[1:]:
        f, _ = os.path.splitext(infile)
        print(f)
        # outfile = f + ".jpg"
        # if infile != outfile:
        #     try:
        #         with Image.open(infile) as im:
        #             im.save(outfile)
        #     except OSError:
        #         print("cannot convert", infile)


to_JPEG()
