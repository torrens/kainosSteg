import math
import zlib
from PIL import Image

def read_text_file(file_path):
    """
    Reads a text file and returns the contents.

    Args:
        file_path (string): Path to text file.

    Returns:
        bytes: The file contents.

    Examples:
        >>> read_text_file('textFile.txt')
        b'x\xda\x95X]o\xdc8\x12|\x8e\x01\xff

    """
    return open(file_path, "rb").read()
    # file = open(file_path, "rb").read(70000)
    # compressed_data = zlib.compress(file, 9)
    # return compressed_data

def write_text_file(data, recovered_secrets):
    """
    Writes data to a file.

    Args:
        data (bytes): Data to be written to a file.
        recovered_secrets (string): File path to write data to.

    Examples:
        >>> write_text_file(data, 'recoveredSecretTextFile.txt')

    """
    f = open(recovered_secrets, 'wb')
    f.write(data)
    f.close()
    # uncompressed_data = zlib.decompress(data)
    # f = open(recovered_secrets, 'wb')
    # f.write(uncompressed_data)
    # f.close()

def read_image_file(file_path):
    """
    Load and return image file.

    Args:
        file_path (string): File path to read.

    Examples:
        >>> read_image_file('someImage.jpg')

    """
    return Image.open(file_path)

def get_pixel_coordinates(index, cols):
    """
    Given a cell index in a grid with x columns, return the column and row of the cell.

                cols

                0   1   2   3

          0  |  0|  1|  2|  3|
             -----------------
    rows  1  |  4|  5|  6|  7|
             -----------------
          2  |  8|  9| 10| 11|
             -----------------
          3  | 12| 13| 14| 15|

    Args:
        index (number): Cell index in a grid, starting from 0.
        cols (number): The number of columns in a grid.

    Returns:
        tuple: The col and row of the cell.

    Examples:
        >>> get_pixel_coordinates(10, 4)
        (2, 2)

    """
    col = index % cols
    row = math.floor(index / cols)
    return col, row

def clear_lsb(byte):
    """
    Clear the least significant bit of a byte.

    Args:
        byte (byte): The byte to have it's LSB set to 0.

    Returns:
        byte: The byte with it's LSB set to 0;

    Examples:
        >>> clear_lsb(0b11111111)
        0b11111110

    """
    bit_mask = 0b11111110
    return byte & bit_mask

def get_bit_from_byte(byte, position):
    """
    Get the bit value of a number.

    Args:
        number (byte): The byte to get the bit from.
        position (int): The bit position to get.  Position is counted from LSB.

    Returns:
        number: The bit value.

    Examples:
        >>> get_bit_from_byte(0b10000000, 7)
        1

    """
    return byte >> position & 1

def set_bit(byte, value, position):
    """
    Set the bit of a number.

    Args:
        byte (number): The number that will be modified.
        value (number): The value to set.
        position (int): The bit position to set.  Position is counted from LSB.

    Returns:
        number: The modified numnber.

    Examples:
        >>> set_bit(0b10000000, 7)
        1

    """
    return byte | ( value << position )

def set_lsb(byte, bit):
    return clear_lsb(byte) + bit

def get_bit_from_byte_array(secret_data, position):
    """
    Get the bit value from a bytes array for a bit at a specific position.

    Args:
        secret_data (bytes): The bytes array to retrieve the bit from.
        position: The bit position in the bytes array.

    Returns:
        number: The bit value of the bit position.

    Examples:
        >>> get_bit_from_byte_array(data, 9)
        1

    """
    byte_index = math.floor(position / 8)
    byte = secret_data[byte_index]
    bit_pos = position - (byte_index * 8)
    return get_bit_from_byte(byte, bit_pos)