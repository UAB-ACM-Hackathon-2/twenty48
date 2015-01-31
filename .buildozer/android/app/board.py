from math import fabs
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout

from block import Block
from util import scale


class Board(FloatLayout):

    locked = False

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        #self.blocks = [Block() for i in range(0, 16)]
        self.blocks = Block()
        self.add_widget(self.blocks)

        self._slide_r = Animation(x=scale.dpx(270))
        self._slide_r.bind(on_complete=self.unlock)
        self._slide_l = Animation(x=0)
        self._slide_l.bind(on_complete=self.unlock)
        self._slide_t = Animation(y=scale.dpy(430))
        self._slide_t.bind(on_complete=self.unlock)
        self._slide_b = Animation(y=0)
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