import sys
from utils import *

def help():
    print("Usage: steg [path to secret image] [path to cover image]")

def validate_input():
    """
    Check that there are two arguments passed to this script.
    """
    args_count = len(sys.argv)
    if args_count != 3:
        help()
        sys.exit()

def combine(secret_image, cover_image, stego_name):
    """
    Store secret data in an image and store the new file.

    Args:
        secret_image (image): The secret image.
        cover_image: (image) The cover image.
        stego_name: (string) File path of new stego image.

    Examples:
        >>> combine(secret_image, cover_image, 'stego.jpg')

    """
    width, height = secret_image.size
    stego = Image.new('RGB', secret_image.size)

    # Hide secret image in cover image
    for x in range(width):
        for y in range(height):

            # Cover image colour values
            c_r, c_g, c_b = cover_image.getpixel((x, y))
            # Secret image colour values
            s_r, s_g, s_b = secret_image.getpixel((x, y))

            # Merge bits
            bit_mask = 0b11110000
            r = (c_r & bit_mask) | (s_r >> 4)
            g = (c_g & bit_mask) | (s_g >> 4)
            b = (c_b & bit_mask) | (s_b >> 4)

            # Write pixel
            stego.putpixel((x, y), (r, g, b))

    print('Creating stego image:', stego_name)
    stego.save(stego_name, "JPEG", quality=100)

def extract(stego_name, secret_name):
    """
    Extract the secret image from the stego image.

    Args:
        stego_image (string): File path of stego image with the secret image hidden.
        secret_name: (string) File path of recovered image.

    Examples:
        >>> extract('stego_hiding_image.jpg', 'secret_image.jpg')

    """
    stego = read_image_file(stego_name)
    width, height = stego.size

    # Create new image to store secret image
    secret = Image.new(stego.mode, stego.size)

    # Extract secret image from stego image
    for x in range(width):
        for y in range(height):

            # Get pixel at x, y co-ordinates
            stego_r, stego_g, stego_b = stego.getpixel((x, y))

            # Extract secret pixel from last 4 bits
            bit_mask = 0b00001111
            r = (stego_r & bit_mask) << 4
            g = (stego_g & bit_mask) << 4
            b = (stego_b & bit_mask) << 4

            # Write pixel
            secret.putpixel((x, y), (r, g, b))

    print('Extracting secret image to:', secret_name)
    secret.save(secret_name, "JPEG")

# Script entry
validate_input()
secret_image_name = sys.argv[1]
cover_image_name = sys.argv[2]

# Read the secret image
secret_image = read_image_file(secret_image_name)

# Read the cover image
cover_image = read_image_file(cover_image_name)

# Create the stego image
combine(secret_image, cover_image, 'generated/stego_hiding_image.jpg')

# Extract the secret image from the stego image
extract('generated/stego_hiding_image.jpg', 'generated/secret_image.jpg')