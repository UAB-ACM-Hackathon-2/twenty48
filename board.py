from math import fabs
from random import randint

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from block import Block


class Slide(Animation):

    _unlock_callback = None

    def __init__(self, **kwargs):
        super(Slide, self).__init__(duration=.25, **kwargs)
        self.bind(on_complete=_unlock_callback)

    @staticmethod
    def set_unlock(callback):
        global _unlock_callback
        _unlock_callback = callback


class Board(FloatLayout):

    locked = False

    def __init__(self, **kwargs):
        self.w = Window.size[0]
        self.h = Window.size[1] - self.w - (Window.size[1] - self.w)/2
        self.d = int(self.w * .25)
        self.grid = self._empty_grid()

        Slide.set_unlock(self._unlock)

        self._slide_r = Slide(x=self._to_gx(3))
        self._slide_l = Slide(x=self._to_gx(0))
        self._slide_t = Slide(y=self._to_gy(3))
        self._slide_b = Slide(y=self._to_gy(0))

        super(Board, self).__init__(**kwargs)
        self.reset()

    def move(self, dx, dy):
        if self.locked:
            return

        self.locked = True

        if fabs(dx) > fabs(dy):
            if dx > 0:
                slide = self._slide_r
            else:
                slide = self._slide_l
        else:
            if dy > 0:
                slide = self._slide_t
            else:
                slide = self._slide_b

        for row in self.grid:
            for block in row:
                if block is None:
                    continue
                block.move(slide)

    def _move_horizontal(self, right):
        r = range(4) if right else range(3, -1, -1)

        for yi in range(4):
            for xi in r:
                print self.grid[yi][xi]

    def _move_vertical(self, up):
        c = range(4) if up else range(3, -1, -1)

        for xi in range(4):
            for yi in c:
                print self.grid[yi][xi]

    def reset(self):
        self._unlock()
        self._spawn_block()
        self._spawn_block()

    def _spawn_block(self):
        x = y = -1
        while x < 0 or y < 0 or not self.grid[x][y] is None:
            x = randint(0, 3)
            y = randint(0, 3)

        self.grid[y][x] = Block(pos=self._to_global(x, y))
        self.add_widget(self.grid[y][x])

    def _unlock(self, *args):
        self.locked = False

    def _to_gx(self, x):
        return self.d*x

    def _to_gy(self, y):
        return self.d*y + self.h

    def _to_global(self, x, y):
        return self._to_gx(x), self._to_gy(y)

    def _to_local(self, x, y):
        return x/self.d, (y - self.h)/self.d

    def _transpose_right(self):
        return self._transpose(3, 0, False)

    def _transpose_left(self):
        return self._transpose(0, 3, False)

    def _transpose_flip(self):
        return self._transpose(0, 3, True)

    def _transpose(self, i_offset, j_offset, flip):
        transpose = self._empty_grid()

        print(self.grid)

        for i in range(4):
            for j in range(4):
                a = i if flip else abs(j_offset - j)
                b = j_offset - j if flip else abs(i_offset - i)
                transpose[a][b] = self.grid[i][j]

        return transpose

    @staticmethod
    def _empty_grid():
        return [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]