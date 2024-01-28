from PIL import Image
from math import floor
import numpy as np
import argparse
import sys

# digits are sorted from lightest to darkest in intensity
# e.g. the darkest pixels map to 0, the brightest pixels map to 7
DIGITS = list(reversed([7, 1, 3, 2, 5, 9, 6, 8, 0]))
"digits are sorted from darkest to brightest"
MONOSPACE = 0.6
"aspect ratio of monospace font characters (height / width)"


def within_threshold(x, target, threshold=0.01):
    """
    Determine if `x` is close enough to the target
    """
    return x <= target and x >= target * (1 - threshold)


def binary_search_floor(nprev, n, target, key=lambda x: x, threshold=0.1):
    """
    Find the maximum value for `n` such that `key(x) >= target`.
    The function `key` must be strictly increasing.
    """
    x = key(n)
    if within_threshold(x, target, threshold):
        return n
    elif x < target:
        return binary_search_floor(n, n*2, target, key, threshold)
    else:
        avg = (n + nprev) / 2
        return binary_search_floor(nprev, avg, target, key, threshold)


def image_to_ascii_digits(filename, max_digits):
    """
    Creat an ascii grid of digits for a given image
    """
    image = Image.open(filename)
    width, height = image.size

    # adjust for the monospace aspect ratio (for most fonts is 0.6)
    new_size = (floor(width / MONOSPACE), height)
    image = image.resize(new_size)
    width, height = image.size

    # The more digits in a number, the longer it takes to determine
    # if it is prime or not, so we limit the ascii image's size.
    # Find a scaling factor that produces an image with no more than
    # the `max_number` of digits.
    scale = binary_search_floor(
        0, 1, max_digits,
        key=lambda x: floor(x**2*width*height),
        threshold=0.0001,
    )

    # resize and greyscale the image
    width = floor(width * scale)
    height = floor(height * scale)
    image = image.resize((width, height)).convert('RGB').convert(mode='L')
    pixels = image.getdata()

    # map each pixel to an ascii digit
    dx = 255 / (len(DIGITS) - 1)
    asc = np.array([
        DIGITS[floor(x / dx)]
        for x in pixels
    ])

    asc.shape = (height, width)
    return asc


def print_ascii(asc, out=print):
    for row in asc:
        out(''.join(map(str, row)))


def default_input(prompt, default):
    response = input(prompt)
    return default if response == '' else response


def file_writer(filename):
    file = open(filename, 'w')
    return lambda x: file.write(x + '\n')


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="AsciiConverter",
        description="Converts an image into an ascii art number",
    )
    parser.add_argument('-i', '--input', help="image file to convert to ascii")
    parser.add_argument('-d', '--digits', help="cap on number of digits in the resulting image", type=int)
    parser.add_argument('-o', '--output', help="path to store ascii art text file", default='')
    return parser


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args(sys.argv[1:])
    filename = args.input
    max_digits = args.digits
    output_filename = args.output
    out = print if output_filename == '' else file_writer(output_filename)

    asc = image_to_ascii_digits(filename, max_digits)
    print_ascii(asc, out)
