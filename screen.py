from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App


class GameScreen(Screen):

    board = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Window.on_keyboard = lambda *x: None

    def on_start_button_pressed(self):
        if self.button.text == 'Start':
            self.button.text = 'Reset'
        else:
            self.button.text = 'Start'

    def on_key_down(self, window, key, *args):
        if key == 273:
            self.board.move(0, 1)
        elif key == 274:
            self.board.move(0, -1)
        elif key == 275:
            self.board.move(1, 0)
        elif key == 276:
            self.board.move(-1, 0)
        elif key in [27, 1000, 1001]:
            App.get_running_app().stop()