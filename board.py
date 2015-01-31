from math import fabs
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from block import Block
from util import scale


class Board(FloatLayout):

    locked = False

    def __init__(self, **kwargs):
        self.w = Window.size[0]
        self.h = Window.size[1] - self.w - (Window.size[1] - self.w)/2
        self.d = int(self.w * .25)

        print self.w
        print self.h
        print self.d
        super(Board, self).__init__(**kwargs)
        #self.blocks = [Block() for i in range(0, 16)]
        self.blocks = Block(value='TEST', pos=self._to_local(0, 0))
        self.add_widget(self.blocks)

        self._slide_r = Animation(x=self._to_x(3))
        self._slide_r.bind(on_complete=self.unlock)
        self._slide_l = Animation(x=self._to_x(0))
        self._slide_l.bind(on_complete=self.unlock)
        self._slide_t = Animation(y=self._to_y(3))
        self._slide_t.bind(on_complete=self.unlock)
        self._slide_b = Animation(y=self._to_y(0))
        self._slide_b.bind(on_complete=self.unlock)

    def move(self, dx, dy):
        if self.locked:
            return

        self.locked = True

        if fabs(dx) > fabs(dy):
            if dx > 0:
                self.blocks.move(self._slide_r)
            else:
                self.blocks.move(self._slide_l)
        else:
            if dy > 0:
                self.blocks.move(self._slide_t)
            else:
                self.blocks.move(self._slide_b)

    def unlock(self, amination, block):
        self.locked = False

    def _to_x(self, x):
        return self.d*x

    def _to_y(self, y):
        return self.d*y + self.h

    def _to_local(self, x, y):
        return self._to_x(x), self._to_y(y)