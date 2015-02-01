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
        Builder.load_file('./block.kv')

        self.set_screen_size()
        return GameScreen()

    @staticmethod
    def get_color_value(value):
        return {
            2: (.929, .891, .852, 1),
            4: (.925, .875, .781, 1),
            8: (.945, .691, .472, 1),
            16: (.957, .582, .386, 1),
            32: (.960, .484, .371, 1),
            64: (.960, .367, .230, 1),
            128: (.926, .808, .445, 1),
            256: (.926, .796, .379, 1),
            512: (.925, .781, .313, 1),
            1024: (1.0, .746, 0.00, 1),
            2048: (1.0, 0.00, 0.00, 1)
        }.get(value, (1, 1, 1, 1))

    @staticmethod
    def get_text_color(value):
        return {
            2: (.074, .429, .394, 1),
            4: (.074, .429, .394, 1),
            8: (.972, .960, .945, 1),
            16: (.972, .960, .945, 1),
            32: (.972, .960, .945, 1),
            64: (.972, .960, .945, 1),
            128: (.972, .960, .945, 1),
            256: (.972, .960, .945, 1),
            512: (.972, .960, .945, 1),
            1024: (.972, .960, .945, 1),
            2048: (.972, .960, .945, 1)
        }.get(value, (0, 0, 0, 1))

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