"""CLI for nametag printer."""
import argparse
from pathlib import Path

from .printer import make_image


def main():
    """Generate a test nametag image."""
    parser = argparse.ArgumentParser(description="Generate nametag test images")
    parser.add_argument("name", help="Name to print on the nametag")
    parser.add_argument(
        "--second-line",
        "-s",
        default=None,
        help="Optional second line of text",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="nametag.png",
        help="Output filename (default: nametag.png)",
    )
    parser.add_argument(
        "--rotate",
        "-r",
        action="store_true",
        help="Rotate image 90 degrees (as it would be printed)",
    )

    args = parser.parse_args()

    # Generate the image
    image = make_image(args.name, args.second_line)

    # Rotate if requested
    if args.rotate:
        image = image.rotate(90, expand=True)

    # Save the image
    output_path = Path(args.output)
    image.save(output_path)

    print(f"Nametag saved to: {output_path.absolute()}")
    print(f"Image size: {image.size[0]}x{image.size[1]} pixels")


if __name__ == "__main__":
    main()
