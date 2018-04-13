import sys

from utils import *

def help():
    print("Usage: python3 file_steg.py [path to text file] [path to image]")

def validate_input():
    """
    Check that there are two arguments passed to this script.
    """
    args_count = len(sys.argv)
    if args_count != 3:
        help()
        sys.exit()

    return sys.argv[1], sys.argv[2]

def combine(header_size, secret_data, cover_image, stego_name):
    """
    Store secret data in an image and store the new file.

    Args:
        header_size (integer): The number of bits to use as a header.
        secret_data (bytes): The bytes array to hide.
        cover_image: (image) The cover image.
        stego: (string) File path of new stego file.

    Examples:
        >>> combine(24, data, image, 'stego.png')

    """
    width, height = cover_image.size

    # Number of bytes * 8 bits in a byte
    secret_data_size = len(secret_data * 8)

    # Header size header_size bits
    for i in range(header_size):
        x, y = get_pixel_coordinates(i, width)
        r, g, b, _ = cover_image.getpixel((x, y))
        modified_g = set_lsb(g, get_bit_from_byte(secret_data_size, i))
        cover_image.putpixel((x, y), (r, modified_g, b))

    # Hide secret data in image
    for i in range(secret_data_size):
        print('todo')
        ##########################################################
        # Very similar code to writing the header above
        # Get x, y co-ordinate values from index and image width
        ##########################################################

        ##########################################################
        # Get r, g, b colour values from pixel at x, y co-ordinates
        ##########################################################

        ##########################################################
        # Set LSB of green colour value
        ##########################################################

        ##########################################################
        # Set the modified pixel at x, y
        ##########################################################

    print('Creating stego image:', stego_name)
    # cover_image.show()
    cover_image.save(stego_name, 'PNG')

def extract(header_size, stego_name, recovered_secrets_name):
    """
    Extract the secret data from the stego image.

    Args:
        header_size (integer): The number of bits that has been used as a header.
        stego (image): The stego image with the secret data.
        recovered_secrets: (string) File path of recovered secrets.

    Examples:
        >>> extract(24, stego, 'recoveredSecretTextFile.txt')

    """
    stego = read_image_file(stego_name)
    width, height = image.size

    secret_data_size = 0

    # Header size header_size bits
    for i in range(header_size):
        x, y = get_pixel_coordinates(i, width)
        r, g, b, _ = stego.getpixel((x, y))
        secret_data_size = set_bit(secret_data_size, get_bit_from_byte(g, 0), i)

    data_bytes = []
    data_byte = 0
    data_bit = 0

    # Extract the secret data
    for i in range(secret_data_size):
        x, y = get_pixel_coordinates(i + header_size, width)
        r, g, b, _ = stego.getpixel((x, y))
        data_byte = set_bit(data_byte, get_bit_from_byte(g, 0), data_bit)
        data_bit += 1
        if data_bit == 8:
            data_bytes.append(data_byte)
            data_bit = 0
            data_byte = 0

    print('Extracting secret data to:', recovered_secrets_name)
    write_text_file(bytes(data_bytes), recovered_secrets_name)

# Script entry
text_file_name, image_file_name = validate_input()

# Read the file to hide
secret_data = read_text_file(text_file_name)

# Read the cover image
image = read_image_file(image_file_name)

# Header size
header_size = 24

# Create the stego image
combine(header_size, secret_data, image, 'generated/stego_hiding_file.png')

# Extract the secret text from the stego image
extract(header_size, 'generated/stego_hiding_file.png', 'generated/secret_file.txt')