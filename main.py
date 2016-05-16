"""
Main
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.logger import Logger

from Menu import Menu, MenuLevel
from EventDispatchers import MenusEventDispatcher
from LevelManager import LevelManager


class MusicProvider(object):
    """
    Music provider.
    """
    sound = None

    def __init__(self):
        """

        :rtype: void
        """
        self.sound = SoundLoader.load('./resources/music/2TalkToMe.wav')

    def start_sound(self):
        """

        :rtype: void
        """
        if self.sound:
            self.sound.play()
            self.sound.loop = True

    def update_sound_state(self, *_):
        """
        Update sound status when player click on music button.

        :rtype: void
        """
        if self.sound.state == 'play':
            self.sound.stop()
            Logger.info("Music stopped.")
        else:
            self.sound.play()
            Logger.info("Music started.")


class GameApp(App):
    """
    Main class of the game.
    """

    LOGO_PATH = './resources/other/logo.png'

    GAME_TITLE = "'Scape Me"

    menus_event_dispatcher = MenusEventDispatcher()
    screen_manager = ScreenManager()
    music_provider = MusicProvider()

    menu_screen = Screen(name="Menu")
    menu_level_screen = Screen(name="MenuLevel")
    game_screen = Screen(name="LevelManager")

    def __init__(self, **kwargs):
        """

        :param kwargs:
        :rtype: void
        """
        super(GameApp, self).__init__(**kwargs)

        self.menu_widget = Menu(self.menus_event_dispatcher, self.music_provider)
        self.menu_screen.add_widget(self.menu_widget)
        self.screen_manager.add_widget(self.menu_screen)

        self.game_widget = LevelManager(self.menus_event_dispatcher, self.music_provider)
        self.game_screen.add_widget(self.game_widget)
        self.screen_manager.add_widget(self.game_screen)

        self.menu_level_widget = MenuLevel(self.menus_event_dispatcher)
        self.menu_level_screen.add_widget(self.menu_level_widget)
        self.screen_manager.add_widget(self.menu_level_screen)

        self.menus_event_dispatcher.bind(on_change_screen=self.do_change_screen)

    def build(self):
        """
        Launch game.

        :rtype: void
        """
        self.music_provider.start_sound()
        self.icon = self.LOGO_PATH
        self.title = self.GAME_TITLE
        self.screen_manager.current = 'Menu'
        return self.screen_manager

    def do_change_screen(self, _, value, *args):
        """
        When player change screen.

        :param _:
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
