from PIL import Image, ImageFilter

FILE_NAME = ''
PX = 90

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

class CubedImage():
    og = None
    final = None
    dimensions = (0, 0)

    def __init__(self, dir, colors, max):
        global COLORS, PX, FILE_NAME
        COLORS, PX, FILE_NAME = colors, max, dir

        self.og = Image.open(FILE_NAME)
        small = self.filter(self.pixellate())
        self.dimensions = small.size
        self.final = small.copy().resize(self.viewing_size(small.size, 1000))

    def pixellate(self):
        copy = self.og.copy()
        copy.thumbnail((PX, PX))

        def nearest(n):
            return n - n % 3

        x, y = copy.size[0], copy.size[1]
        rect = (0, 0, nearest(x), nearest(y))
        return copy.crop(rect)

    def filter(self, img):
        source = img.split()
        masks = self.gen_masks(img)

        for color in range(len(COLORS)):
            for rgb in range(3):
                c = source[rgb].point(lambda i: COLORS[color][rgb])
                source[rgb].paste(c, None, masks[color])
        return Image.merge(img.mode, source)

    def gen_masks(self, img):
        img = img.convert("L")
        source = img.split()
        masks = []

        def add_section(lower, higher):
            masks.append(source[0].point(lambda i: (i >= lower and i <= higher) and 255))

        for a, b in BOUNDS[len(COLORS)]:
            add_section(a, b)
        return masks

    def viewing_size(self, xy, max_d):
        factor = max_d // max(xy)
        return ([factor * d for d in xy])
