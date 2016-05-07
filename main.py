from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

from Menu import Menu, MenuLevel
from Configurations import textures, authorizations
from EventDispatchers import MenusEventDispatcher
from LevelManager import LevelManager


class GameApp(App):
    # sound = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        super(GameApp, self).__init__(**kwargs)
        self.textures = textures
        self.authorizations = authorizations
        self.my_event_dispatcher = MenusEventDispatcher()
        self.screen_manager = ScreenManager()

        self.menu_widget = Menu(self.my_event_dispatcher)
        self.menu_screen = Screen(name="Menu")
        self.menu_screen.add_widget(self.menu_widget)
        self.screen_manager.add_widget(self.menu_screen)

        self.game_widget = LevelManager()
        self.game_screen = Screen(name="LevelManager")
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

        self.menu_level_widget = MenuLevel(self.my_event_dispatcher)
        self.menu_level_screen = Screen(name="MenuLevel")
        self.menu_level_screen.add_widget(self.menu_level_widget)
        self.screen_manager.add_widget(self.menu_level_screen)

        self.my_event_dispatcher.bind(on_change_screen=self.do_change_screen)

    def build(self):
        """
        Launch game.

        :rtype: void
        """

        # self.sound = SoundLoader.load('resources/music/test.mp3')
        # if self.sound:
        #     self.sound.play()

        self.icon = './resources/other/logo.png'
        self.title = "'Scape Me"
        self.game_widget.load_set()
        self.screen_manager.current = 'LevelManager'
        return self.screen_manager

    def do_change_screen(self, instance, value, *args):
        """
        When player change screen.

        :param instance:
        :param value:
        :param args:
        :rtype: void
        """
        self.screen_manager.current = value

    def on_pause(self):
        return True


if __name__ == '__main__':
    GameApp().run()
