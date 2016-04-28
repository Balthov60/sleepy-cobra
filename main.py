from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Level import Level
from Menu import Menu
from Textures import textures, authorizations


class GameApp(App):
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        super(GameApp, self).__init__(**kwargs)
        self.textures = textures
        self.authorizations = authorizations
        self.screen_manager = ScreenManager()

        self.menu_widget = Menu()
        self.menu_screen = Screen(name="Menu")
        self.menu_screen.add_widget(self.menu_widget)
        self.screen_manager.add_widget(self.menu_screen)

        self.game_widget = Level('resources/maps/test.cfg', self.textures, self.authorizations)
        self.game_screen = Screen(name="Game")
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

    def build(self):
        """

        :return:
        """
        self.screen_manager.current = 'Game'
        return self.screen_manager

if __name__ == '__main__':
    GameApp().run()
