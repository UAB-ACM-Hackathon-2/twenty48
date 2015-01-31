from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout


class Block(AnchorLayout):

    value = StringProperty()

    def __init__(self, value=0, pos=(0, 0), **kwargs):
        self.w = Window.size[0]*.25
        self.value = str(value)
        super(Block, self).__init__(**kwargs)
        self.pos = pos

    def move(self, animation):
        animation.start(self)

    def destroy(self):
        self.parent.remove_widget(self)