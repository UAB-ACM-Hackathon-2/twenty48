# this must be first
from kivy import Config

Config.set('kivy', 'log_level', 'info')  # info, debug, or warning
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')

from kivy.app import App, platform
from kivy.lang import Builder
from kivy.core.window import Window

from screen import GameScreen
from util import scale


__version__ = '0.1'


class Twenty48(App):

    def build(self):
        Builder.load_file('./screen.kv')
        Builder.load_file('./board.kv')
        Builder.load_file('./block.kv')

        self.set_screen_size()
        return GameScreen()

    @staticmethod
    def set_screen_size():
        w = Config.getint('graphics', 'width')
        h = Config.getint('graphics', 'height')
        dim = Window.size

        if platform not in ('ios', 'android'):
            Window.size = (w, h)

        scalex = dim[0]/float(w)
        scaley = dim[1]/float(h)
        scale.set_scale(scalex, scaley)


if __name__ == '__main__':
    Twenty48().run()