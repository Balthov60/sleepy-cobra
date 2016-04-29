from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Level import Level
from Menu import Menu
from Configurations import textures, authorizations
from FilesUtils import get_object_from_yaml, set_object_in_yaml, test_yaml_file


class GameApp(App):

    SAVE_PATH = "resources/save.yml"
    group_path = ['player_save', 'group']
    level_path = ['player_save', 'level']

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

        test_yaml_file(self.SAVE_PATH)
        self.group = get_object_from_yaml(self.SAVE_PATH, self.group_path)
        self.level = get_object_from_yaml(self.SAVE_PATH, self.level_path)

        if self.group is None or self.group == 0:
            set_object_in_yaml(self.SAVE_PATH, ['player_save', 'group'], 1)
            self.group = 1

        if self.level is None or self.group == 0:
            set_object_in_yaml(self.SAVE_PATH, ['player_save', 'level'], 1)
            self.group = 1

        self.game_widget = Level(self.group, self.level, self.textures, self.authorizations)
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
