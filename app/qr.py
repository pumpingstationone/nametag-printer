import sys
import os
import epaper
from PIL import Image, ImageDraw, ImageFont
import time


def main():
    try:
        # Initialize the e-paper display
        epd = epaper.epaper('epd4in2_V2').EPD()
        epd.init()
        epd.Clear()  # Clear the display

        # Create a blank image for drawing
        # The display resolution is 400x300
        image = Image.new('1', (epd.width, epd.height), 255)  # 1-bit mode, white background
        draw = ImageDraw.Draw(image)

        # Load a font
        font_path = 'OpenSans-Regular.ttf'  # Adjust path if necessary
        font = ImageFont.truetype(font_path, 24)

        # Draw some text
        text = "Hello, Waveshare!"

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (epd.width - text_width) // 2  # Center horizontally
        text_y = (epd.height - text_height) // 2  # Center vertically
        draw.text((text_x, text_y), text, font=font, fill=0)  # Black text

        # Display the image on the e-paper
        epd.display(epd.getbuffer(image))
        time.sleep(5)  # Keep the text displayed for 5 seconds

        # Put the display to sleep
        epd.sleep()

    except KeyboardInterrupt:
        print("Exiting...")
        epd.epdconfig.module_exit()
        sys.exit()


if __name__ == "__main__":
    main()
