from PIL import Image, ImageDraw
import argparse
import sys

# Window bounds
REAL_START = -2
REAL_END = 1
IMAG_START = -1.5
IMAG_END = 1.5

ITER_LIM = 100

def mandelbrot(c):
    """
    Count iterations to convergence.
    """
    z = 0
    iterations = 0
    while abs(z) <= 2 and iterations < ITER_LIM:
        z = z * z + c
        iterations += 1
    return iterations

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='path', default='output.png', help='path to which to output image')
    parser.add_argument('-s', dest='size', type=int, default=400, help='resolution of output image')
    args = parser.parse_args()

    width = args.size
    height = args.size

    image = Image.new('HSV', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for x in range(0, width):
        sys.stdout.write('\033[K')
        print('x=%d/%d (%d%%)\r' % (x, width, 100*x/width), end='')
        sys.stdout.flush()
        for y in range(0, height//2+1):
            # Get complex number from coordinate
            c = complex(REAL_START + (x / width) * (REAL_END - REAL_START),
                        IMAG_START + (y / height) * (IMAG_END - IMAG_START))
            iterations = mandelbrot(c)
            hsv = (140,
                   255,
                   int(255 * iterations / ITER_LIM) if iterations < ITER_LIM else 0)
            draw.point([x, y], hsv)
            draw.point([x, height - y], hsv)

    image.convert('RGB').save(args.path, 'PNG')
    print('Image successfully saved to %s.' % args.path)
