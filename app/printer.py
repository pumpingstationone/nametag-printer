
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster
from brother_ql.backends.helpers import send, discover


def print_name(name: str) -> str:
    image = make_image(name)

    # Show the image (debug)
    image.show()

    # Rotate the image 90 degrees
    image.rotate(90, expand=True)

    # Uncomment the line below to actually print
    # print_image(image)


def print_image(image: Image.Image):
    # Auto-discover the printer using the pyusb backend
    printer_id = discover('pyusb')[0]['identifier']

    # Discard broken serial from identifier
    # https://github.com/pklaus/brother_ql_web/issues/10#issuecomment-994990935
    printer_id = printer_id.split("_")[0]

    # Need to create new qlr object for each print
    qlr = BrotherQLRaster("QL-800")
    qr_data = convert(qlr, [image], "60x86")
    send(qr_data, printer_id)


def make_image(name: str) -> Image.Image:
    """Generate a nametag image with the given name."""

    # Path to the font file
    font_path = "OpenSans-Regular.ttf"

    # Define image dimensions
    image_width = 954
    image_height = 672

    # Define black bar heights
    top_bar_height = 200
    bottom_bar_height = 100

    # Define text positions
    hello_text_y = 0
    my_name_is_text_y = 115

    # Create a blank white image
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_name_size = 170
    font_hello_size = 100
    font_my_name_is_size = 50

    try:
        font_hello = ImageFont.truetype(font_path, font_hello_size)
        font_my_name_is = ImageFont.truetype(font_path, font_my_name_is_size)
    except IOError:
        # Fallback to default fonts
        font_hello = ImageFont.load_default(font_hello_size)
        font_my_name_is = ImageFont.load_default(font_my_name_is_size)

    # Dynamically adjust font size for the name
    while True:
        try:
            font_name = ImageFont.truetype(font_path, font_name_size)
        except IOError:
            font_name = ImageFont.load_default(font_name_size)

        text_bbox = draw.textbbox((0, 0), name, font=font_name)
        text_width = text_bbox[2] - text_bbox[0]

        # Leave a margin on both sides
        if text_width <= image_width - 100:
            break

        # Decrease font size if text is too wide
        font_name_size -= 5

    # Add black bars at the top and bottom
    draw.rectangle([(0, 0), (image_width, top_bar_height)], fill="black")
    draw.rectangle([(0, image_height - bottom_bar_height), (image_width, image_height)], fill="black")

    # Add "Hello" text
    hello_text = "Hello"
    hello_bbox = draw.textbbox((0, 0), hello_text, font=font_hello)
    hello_width = hello_bbox[2] - hello_bbox[0]
    hello_x = (image_width - hello_width) // 2
    draw.text((hello_x, hello_text_y), hello_text, fill="white", font=font_hello)

    # Add "my name is" text
    my_name_is_text = "my name is"
    my_name_is_bbox = draw.textbbox((0, 0), my_name_is_text, font=font_my_name_is)
    my_name_is_width = my_name_is_bbox[2] - my_name_is_bbox[0]
    my_name_is_x = (image_width - my_name_is_width) // 2
    draw.text((my_name_is_x, my_name_is_text_y), my_name_is_text, fill="white", font=font_my_name_is)

    # Calculate text position to center the name within the white space
    white_space_top = top_bar_height
    white_space_bottom = image_height - bottom_bar_height
    white_space_height = white_space_bottom - white_space_top

    # Adjust for font ascent and descent
    ascent, descent = font_name.getmetrics()
    visual_text_height = ascent + descent

    text_x = (image_width - text_width) // 2
    text_y = white_space_top + (white_space_height - visual_text_height) // 2

    # Draw the name on the image
    draw.text((text_x, text_y), name, fill="black", font=font_name)

    return image


