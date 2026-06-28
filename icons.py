import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = "#004e42"
ICON_COLOR = "#ffcd00"
IMAGE_SIZE = 256
FONT_SIZE = 160 # the icons are fonts

# Super sampling anti aliasing
SCALE = 4
DRAW_SIZE = IMAGE_SIZE * SCALE
SCALED_FONT_SIZE = FONT_SIZE * SCALE

# get unicode from Code Point heading at https://icons.getbootstrap.com/icons/bootstrap/ for example
ICONS = {
    "email": "\uF32C", # bi-envelope-fill
    "link-45deg": "\uF470", # bi-link-45deg
    "linkedin": "\uF472", # bi-linkedin
    "instagram": "\uF437", # bi-instagram
    "discord": "\uF300", # bi-discord
    "globe": "\uF3EE" # bi-globe
}

FONT_URL = "https://raw.githubusercontent.com/twbs/icons/main/font/fonts/bootstrap-icons.woff"
FONT_PATH = "bootstrap-icons.woff"

OUTPUT_DIR = "icons"

def main():
    try:
        # Load the font at the scaled-up size
        font = ImageFont.truetype(FONT_PATH, SCALED_FONT_SIZE)
    except IOError:
        print("Error loading font, downloading from github")
        urllib.request.urlretrieve(FONT_URL, FONT_PATH)
        font = ImageFont.truetype(FONT_PATH, SCALED_FONT_SIZE)

    os.makedirs(OUTPUT_DIR, exist_ok=True) # output directory

    for name, unicode in ICONS.items():
        img = Image.new("RGBA", (DRAW_SIZE, DRAW_SIZE), (255, 255, 255, 0)) # make transparent background image
        draw = ImageDraw.Draw(img)

        draw.ellipse((0, 0, DRAW_SIZE, DRAW_SIZE), fill=BG_COLOR) # draw circle background

        center_x = DRAW_SIZE / 2
        center_y = DRAW_SIZE / 2

        draw.text((center_x, center_y), unicode, font=font, fill=ICON_COLOR, anchor="mm") # center with middle-middle anchor

        final_img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.BILINEAR) # shrink

        # Save out the high-res PNG
        filepath = f"{OUTPUT_DIR}/{name}.png"
        final_img.save(filepath)
        print(f"Wrote {filepath}")

if __name__ == "__main__":
    main()