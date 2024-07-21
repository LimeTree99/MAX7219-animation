from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text

import time
from copy import deepcopy


BLACK = b'\x00\x00\x00'
WHITE = b'\xff\xff\xff'
BYTE_SIZE = 8


class Screen:
    def __init__(self, port=0, device=0):
        self.serial = spi(port=port, device=device, gpio=noop())
        self.device = max7219(self.serial)

    def letter(self, letter):
        with canvas(self.device) as draw:
            text(draw, (1,1), letter, fill='white')

    def points(self, points):
        with canvas(self.device) as draw:
            draw.point(points, fill='white')
    
    def line(self, a, b):
        with canvas(self.device) as draw:
            draw.line(a, b, fill='white')


class Grid:
    ON = 1
    OFF = 0
    def __init__(self, width, height, bmp=None):
        self.width = width
        self.height = height
        self._empty = [[Grid.OFF for _ in range(self.width)] for _ in range(self.height)]
        self.grid = deepcopy(self._empty)

        if bmp != None:
            self.import_bmp(bmp)
    
    def print(self):
        for line in self.grid:
            print(line)

    def clear(self):
        self.grid = deepcopy(self._empty)

    def add(self, point):
        self.grid[point[1]][point[0]] = Grid.ON

    def delete(self, point):
        self.grid[point[1]][point[0]] = Grid.OFF

    def imp_grid(self, grid):
        self.grid = grid

    def list(self):
        'converts a 2D grid matrix to a list of points'
        points = []
        for y in range(self.width):
            for x in range(self.height):
                if self.grid[y][x] == Grid.ON:
                    points.append((x,y))
        return points

    def import_bmp(self, f_name, color=BLACK):
        fh = open(f_name, 'rb')
        bmp = fh.read()
        fh.close()

        size = int.from_bytes(bmp[2:6], 'little')
        offset = int.from_bytes(bmp[10:14], 'little')
        width = int.from_bytes(bmp[18:22], 'little')
        height = int.from_bytes(bmp[22:26], 'little')
        pix_depth = int.from_bytes(bmp[28:30], 'little')
        pix_depth = pix_depth // BYTE_SIZE

        i=0
        for y in range(height-1, -1, -1):
            for x in range(width):
                bit_pos = offset + (i * pix_depth)
                pixel = bmp[bit_pos:bit_pos+pix_depth]
                
                if pixel == color:
                    self.add((x,y))
                else:
                    self.delete((x,y))
                i += 1


class Animate:
    def __init__(self, screen, fps=30, clear_s=False, width=8, height=8):
        self.screen = screen
        self.running = True
        
        self.fps=fps
        self.clear_s = clear_s

        self.grid = Grid(width, height)
        self.frames = []
        self.frame_p = -1
        self.frame_count = 0

    def update(self):
        self.grid = self.frames[self.frame_p]
        self.frame_p = (self.frame_p + 1) % self.frame_count

    def run(self):
        while self.running:
            if self.clear_s:
                self.grid.clear()

            self.update()

            points = self.grid.list()
            self.screen.points(points)

            time.sleep(1/self.fps)
    
    def add_frames(self, f_list):
        for f_name in f_list:
            frame = Grid(self.grid.width, self.grid.height, bmp=f_name)
            self.frames.append(frame)
            self.frame_count += 1

        if len(self.frames) > 0:
            self.frame_p = 0


