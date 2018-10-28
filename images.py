from PIL import Image, ImageFilter

FILE_NAME = 'whale.jpg'
PX = 132

# rgb
BLUE = (37, 37, 221)
GREEN = (42, 128, 42)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 226, 40)
WHITE = (255, 255, 255)

COLORS = [BLUE, GREEN, RED, ORANGE, YELLOW, WHITE]

BOUNDS = { # grayscale
    1: [(0, 255)],
    2: [(0, 127), (128, 255)],
    3: [(0, 84), (85, 139), (140, 255)],
    4: [(0, 75), (76, 100), (101, 149), (150, 255)],
    5: [(0, 70), (71, 84), (85, 124), (125, 159), (160, 255)],
    6: [(0, 35), (36, 49), (50, 99), (100, 139), (140, 169), (170, 255)]
}

def viewing_size(xy, max_d):
    factor = max_d // max(xy)
    return ([10 * d for d in xy])

def pixellated(img):
    copy = img.copy()
    copy.thumbnail((PX, PX))

    def nearest(n):
        return n - n % 3

    x, y = copy.size[0], copy.size[1]
    rect = (0, 0, nearest(x), nearest(y))
    return copy.crop(rect)

def gen_masks(img):
    img = img.convert("L")
    source = img.split()
    masks = []

    def add_section(lower, higher):
        masks.append(source[0].point(lambda i: (i >= lower and i <= higher) and 255))

    for a, b in BOUNDS[len(COLORS)]:
        add_section(a, b)
    return masks

def filtered(img):
    source = img.split()
    masks = gen_masks(img)

    for color in range(len(COLORS)):
        for rgb in range(3):
            c = source[rgb].point(lambda i: COLORS[color][rgb])
            source[rgb].paste(c, None, masks[color])
    img = Image.merge(img.mode, source)
    return img

im = Image.open(FILE_NAME)
small = filtered(pixellated(im))
print(small.size)
big = small.copy().resize(viewing_size(small.size, 1000))
big.show()
