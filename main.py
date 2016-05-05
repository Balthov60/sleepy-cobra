from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Level import Level
from Menu import Menu, MenuLevel
from Configurations import textures, authorizations
from MyEventDispatcher import MenusEventDispatcher


class GameApp(App):
    def do_change_screen(self, instance, value, *args):
        """

        :param instance:
        :param value:
        :param args:
        :rtype: void
        """
        self.screen_manager.current = value

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

        self.game_widget = Level(self.textures, self.authorizations)
        self.game_screen = Screen(name="Game")
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

        self.menu_level_widget = MenuLevel(self.my_event_dispatcher)
        self.menu_level_screen = Screen(name="Menu_level")
        self.menu_level_screen.add_widget(self.menu_level_widget)
        self.screen_manager.add_widget(self.menu_level_screen)

        self.my_event_dispatcher.bind(on_change_screen=self.do_change_screen)

    def build(self):
        """

        :return:
        """
        self.screen_manager.current = 'Menu'
        return self.screen_manager


if __name__ == '__main__':
    GameApp().run()
