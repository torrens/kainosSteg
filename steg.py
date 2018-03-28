import sys

from utils import *

def help():
    print("Usage: steg [path to text file] [path to image]")

def validate_input():
    """
    Check that there are two arguments passed to this script.
    """
    args_count = len(sys.argv)
    if args_count != 3:
        help()
        sys.exit()

def combine(header_size, secret_data, image, stego):
    """
    Store secret data in an image and store the new file.

    Args:
        secret_data (bytes): The bytes array to hide.
        image: (image) The cover image.
        stego: (string) File path of new stego file.

    Examples:
        >>> combine(data, image, 'stego.png')

    """
    pixels = image.load()
    width, height = image.size

    # Number of bytes * 8 bits in a byte
    secret_data_size = len(secret_data * 8)

    # Header size header_size bits
    for i in range(header_size):
        x, y = get_pixel_coordinates(i, width)
        r, g, b = image.getpixel((x, y))
        modified_g = set_lsb(g, get_bit_from_byte(secret_data_size, i))
        pixels[x, y] = (r, modified_g, b)

    # Hide secret data in image
    for i in range(secret_data_size):
        x, y = get_pixel_coordinates(i + header_size, width)
        r, g, b = image.getpixel((x, y))
        modified_g = set_lsb(g,  get_bit_from_byte_array(secret_data, i))
        pixels[x, y] = (r, modified_g, b)

    print('Creating stego image:', stego)
    image.save(stego)

def extract(header_size, stego, recovered_secrets):
    """
    Extract the secret data from the stego image.

    Args:
        stego (image): The stego image with the secret data.
        recovered_secrets: (string) File path of recovered secrets.

    Examples:
        >>> extract(stego, 'recoveredSecretTextFile.txt')

    """
    pixels = read_image_file(stego).load()
    width, height = image.size

    secret_data_size = 0

    # Header size header_size bits
    for i in range(header_size):
        x, y = get_pixel_coordinates(i, width)
        r, g, b = image.getpixel((x, y))
        secret_data_size = set_bit(secret_data_size, get_bit_from_byte(g, 0), i)

    data_bytes = []
    data_byte = 0
    data_bit = 0

    # Extract the secret data
    for i in range(secret_data_size):
        x, y = get_pixel_coordinates(i + header_size, width)
        r, g, b = image.getpixel((x, y))
        data_byte = set_bit(data_byte, get_bit_from_byte(g, 0), data_bit)
        data_bit += 1
        if data_bit == 8:
            data_bytes.append(data_byte)
            data_bit = 0
            data_byte = 0

    print('Extracting secret data to:', recovered_secrets)
    write_text_file(bytes(data_bytes), recovered_secrets)

# Script entry
validate_input()
text_file = sys.argv[1]
image_file = sys.argv[2]

# Read the file to hide
secret_data = read_text_file(text_file)

# Read the cover image
image = read_image_file(image_file)

# Header size
header_size = 24

# Create the stego image
combine(header_size, secret_data, image, 'generated/stego.jpg')

# Extract the secret text from the stego image
extract(header_size, 'generated/stego.jpg', 'generated/recoveredSecretTextFile.txt')