from kivy.properties import NumericProperty
from kivy.uix.button import Button

from util import scale


class Block(Button):

    value = NumericProperty()

    def __init__(self, value=0, **kwargs):
        self.value = value
        super(Block, self).__init__(**kwargs)
        self.pos = (0, 0)
        self.size = (scale.dpy(50), scale.dpy(50))
        self.size_hint = (None, None)
        self.text = str(self.value)

    def move(self, animation):
        animation.start(self)