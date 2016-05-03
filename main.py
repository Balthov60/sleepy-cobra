from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from LevelManager import LevelManager
from Menu import Menu


class GameApp(App):
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        super(GameApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()

        self.menu_widget = Menu()
        self.menu_screen = Screen(name="Menu")
        self.menu_screen.add_widget(self.menu_widget)
        self.screen_manager.add_widget(self.menu_screen)

        self.game_widget = LevelManager()
        self.game_screen = Screen(name="LevelManager")
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

    def build(self):
        """

        :return:
        """
        self.game_widget.load_resuming_level()
        self.screen_manager.current = 'LevelManager'
        return self.screen_manager


if __name__ == '__main__':
    GameApp().run()
