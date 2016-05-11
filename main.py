from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

from Menu import Menu, MenuLevel
from EventDispatchers import MenusEventDispatcher
from LevelManager import LevelManager


class GameApp(App):
    sound = None

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :rtype: void
        """
        super(GameApp, self).__init__(**kwargs)
        self.menus_event_dispatcher = MenusEventDispatcher()
        self.screen_manager = ScreenManager()

        self.menu_widget = Menu(self.menus_event_dispatcher)
        self.menu_screen = Screen(name="Menu")
        self.menu_screen.add_widget(self.menu_widget)
        self.screen_manager.add_widget(self.menu_screen)

        self.game_widget = LevelManager(self.menus_event_dispatcher)
        self.game_screen = Screen(name="LevelManager")
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

        self.menu_level_widget = MenuLevel(self.menus_event_dispatcher)
        self.menu_level_screen = Screen(name="MenuLevel")
        self.menu_level_screen.add_widget(self.menu_level_widget)
        self.screen_manager.add_widget(self.menu_level_screen)

        self.menus_event_dispatcher.bind(on_change_screen=self.do_change_screen)

    def build(self):
        """
        Launch game.

        :rtype: void
        """

        self.sound = SoundLoader.load('./resources/other/2TalkToMe.mp3')
        if self.sound:
            self.sound.play()
            self.sound.loop = True

        self.icon = './resources/other/logo.png'
        self.title = "'Scape Me"
        self.screen_manager.current = 'Menu'
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

        # when load level
        if args[0]:
            self.game_widget.load_level_in_set(args[0])

    def on_pause(self):
        """
        Required method
        """
        return True

if __name__ == '__main__':
    GameApp().run()
