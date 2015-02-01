import copy
from math import fabs
from random import randint

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from block import Block


class Overlay(FloatLayout):
    start = 'Press Start'
    win = 'You Win!\n(Press Reset)'
    lose = 'You Lose!\n(Press Reset)'


class Slide(Animation):
    _unlock_callback = None

    def __init__(self, block, **kwargs):
        super(Slide, self).__init__(duration=.125, **kwargs)
        self.block = block
        self.bind(on_complete=_unlock_callback)

    @staticmethod
    def set_unlock_callback(callback):
        global _unlock_callback
        _unlock_callback = callback


class Board(FloatLayout):

    locked = False

    def __init__(self, **kwargs):
        self.w = Window.size[0]
        self.h = Window.size[1] - self.w - (Window.size[1] - self.w) / 2
        self.d = int(self.w * .25)
        self.grid = self._empty_grid()
        self.slide_queue = []
        self.overlay = Overlay(pos=(0, self.h), size=(self.w, self.w))

        Slide.set_unlock_callback(self._unlock)

        super(Board, self).__init__(**kwargs)
        self.reset()
        self.end = True

    def on_touch_move(self, touch):
        self.move(touch.dsx, touch.dsy)

    def move(self, dx, dy):
        if self.end or self.locked:
            return

        self.locked = True

        if fabs(dx) > fabs(dy):
            if dx > 0:
                direction = 0
                rotate = lambda: self.grid
                unrotate = lambda: self.grid
            else:
                direction = 1
                rotate = self._transpose_flip
                unrotate = self._transpose_flip
        else:
            if dy > 0:
                direction = 2
                rotate = self._transpose_left
                unrotate = self._transpose_right
            else:
                direction = 3
                rotate = self._transpose_right
                unrotate = self._transpose_left

        old = self._snapshot()

        g = rotate()
        self.grid = self._move(g, direction)
        self.grid = unrotate()

        if self.gameover(old):
            self.end = True
            self.overlay.text = self.overlay.lose

        for slide in self.slide_queue:
            #print '%s\t%s' % (self._to_local(slide.block.x, slide.block.y), slide.animated_properties)
            slide.start(slide.block)
        self.slide_queue = []
        #print '-----'

    def _move(self, grid, dir):
        g = self._empty_grid()

        for yi in range(4):
            row = []
            for xi in range(4):
                if not grid[yi][xi] is None:
                    row.append(grid[yi][xi])
            g[yi] = self._collapse(row, dir)

        return g

    def _collapse(self, irow, dir):
        row = []

        horizontal = dir < 2
        pos = dir % 2 == 0

        if len(irow) > 1:
            merge = 4
            i = len(irow) - 1
            j = 3
            while i >= 0:
                if irow[i].value == irow[i-1].value and merge != i:
                    row.append(Block(value=irow[i].value * 2))
                    if horizontal:
                        self.slide_queue.append(Slide(irow[i], x=self._to_gx(j if pos else 3-j)))
                        self.slide_queue.append(Slide(irow[i-1], x=self._to_gx(j if pos else 3-j)))
                    else:
                        self.slide_queue.append(Slide(irow[i], y=self._to_gy(j if pos else 3-j)))
                        self.slide_queue.append(Slide(irow[i-1], y=self._to_gy(j if pos else 3-j)))
                    merge = i
                    i -= 1
                else:
                    row.append(Block(value=irow[i].value))
                    if horizontal:
                        self.slide_queue.append(Slide(irow[i], x=self._to_gx(j if pos else 3-j)))
                    else:
                        self.slide_queue.append(Slide(irow[i], y=self._to_gy(j if pos else 3-j)))
                i -= 1
                j -= 1
        elif len(irow) == 1:
            row.append(Block(value=irow[0].value))
            if horizontal:
                self.slide_queue.append(Slide(irow[0], x=self._to_gx(3 if pos else 0)))
            else:
                self.slide_queue.append(Slide(irow[0], y=self._to_gy(3 if pos else 0)))

        while len(row) < 4:
            row.append(None)

        row.reverse()
        return row

    def gameover(self, old):
        print old
        print self.grid
        for x in range(4):
            for y in range(4):
                if old[x][y] != self.grid[x][y] or (not old[x][y] is None and old[x][y].value != self.grid[x][y].value):
                    return False
        return True

    def is_full(self):
        for x in range(4):
            for y in range(4):
                if self.grid[x][y] is None:
                    return False
        return True

    def reset(self):
        self.end = False
        self.locked = True
        self._unlock()
        self._spawn_block()
        self.add_widget(self.overlay)

    def _spawn_block(self):
        if self.is_full():
            return

        x = y = -1
        while x < 0 or y < 0 or not self.grid[y][x] is None:
            x = randint(0, 3)
            y = randint(0, 3)

        self.grid[y][x] = Block(pos=self._to_global(x, y), value=2)
        self.add_widget(self.grid[y][x])

    def _unlock(self, *args):
        if not self.locked:
            return

        self.locked = False

        self.clear_widgets()
        for y in range(4):
            for x in range(4):
                if self.grid[y][x] is not None:
                    self.grid[y][x].pos = self._to_global(x, y)
                    self.add_widget(self.grid[y][x])

        self._spawn_block()

    def _to_gx(self, x):
        return self.d * x

    def _to_gy(self, y):
        return self.d * y + self.h

    def _to_global(self, x, y):
        return self._to_gx(x), self._to_gy(y)

    def _to_local(self, x, y):
        return x / self.d, (y - self.h) / self.d

    def _transpose_right(self):
        return self._transpose(3, 0, False)

    def _transpose_left(self):
        return self._transpose(0, 3, False)

    def _transpose_flip(self):
        return self._transpose(0, 3, True)

    def _transpose(self, i_offset, j_offset, flip):
        transpose = self._empty_grid()

        for i in range(4):
            for j in range(4):
                a = i if flip else abs(j_offset - j)
                b = j_offset - j if flip else abs(i_offset - i)
                transpose[a][b] = self.grid[i][j]

        return transpose

    def _snapshot(self):
        g = self._empty_grid()
        for x in range(4):
            for y in range(4):
                g[x][y] = None if self.grid[x][y] is None else Block(self.grid[x][y].value)
        return g

    @staticmethod
    def _empty_grid():
        return [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
