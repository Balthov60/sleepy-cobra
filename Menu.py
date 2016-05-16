"""
Menu
"""
import os

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.logger import Logger

from LevelService import LevelService
from Configurations import COLORS
from EventDispatchers import propagate_event
from PopUpProvider import open_pop_up


class Menu(RelativeLayout):
    """
    Main menu class.
    """
    FONT_MENU_PATH = './resources/menu/vanadine_bold.ttf'
    FOND_MENU_PATH = './resources/menu/background_menu.png'
    LOGO_PATH = './resources/other/logo.png'

    def __init__(self, event_dispatcher, music, **kwargs):
        """
        Initialize menu's button and textures.
        :param event_dispatcher: dispatcher
        :param kwargs: Args of Layout
        :rtype: void
        """
        super(Menu, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.music = music

        # Add fond and title.
        self.canvas.add(
            Rectangle(source=self.FOND_MENU_PATH, size=Window.size)
        )

        self.canvas.add(
            Rectangle(
                source=self.LOGO_PATH,
                size_hint=0.2,
                pos_hint={'x': 0.4, 'y': 0.4}
            )
        )
        self.add_widget(
            Label(
                text="'Scape me",
                font_name=self.FONT_MENU_PATH,
                font_blended=False,
                font_size='87sp',
                size_hint=(0.25, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.8}
            )
        )

        # Add buttons.
        self.add_widget(
            Button(
                text="Play !",
                font_name=self.FONT_MENU_PATH,
                font_size='80sp',
                background_color=(0, 0, 0, 0),
                size_hint=(.45, .15),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                on_press=self.switch_to_menu_level_screen
            )
        )

        self.add_widget(
            Button(
                text="Credits",
                font_name=self.FONT_MENU_PATH,
                font_size='40sp',
                background_color=(0, 0, 0, 0),
                pos_hint={'center_x': 0.5, 'center_y': 0.2},
                size_hint=(.2, .2),
                on_press=self.credit_button_callback
            )
        )

        self.add_widget(
            Button(
                text="Music",
                font_name=self.FONT_MENU_PATH,
                font_size='25sp',
                background_color=(0, 0, 0, 0),
                size_hint=(0.15, 0.12),
                pos_hint={'center_x': 0.90, 'center_y': 0.06},
                on_press=self.music_callback
            )
        )

    def switch_to_menu_level_screen(self, *_):
        """
        Propagation method.
        :param _:
        :return:
        """
        Logger.info("Propagate MenuLevel")
        propagate_event('MenuLevel', self)

    def credit_button_callback(self, _):
        """
        When player click on credit button (Required method).
        :param _:
        :rtype: void
        """
        open_pop_up(self, 'Credits')

    def music_callback(self, _):
        """
        Start/Stop music.
        :param _:
        :rtype: void
        """
        self.music.update_sound_state()


class MenuLevel(FloatLayout):
    """
    Level Menu class.
    """
    FONT_MENU_PATH = './resources/menu/vanadine_bold.ttf'
    FOND_MENU_PATH = './resources/menu/background_menu.png'
    MAPS_PATH = './resources/maps/'

    color_1 = COLORS['blue_color']
    color_2 = COLORS['dark_blue_color']

    def __init__(self, event_dispatcher, **kwargs):
        """
        Initialize button and textures of MenuLevel.
        :param event_dispatcher: dispatcher
        :param kwargs: args of layout
        :rtype: void
        """
        super(MenuLevel, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.level_service = LevelService()

        # Add fond.
        self.canvas.add(
            Rectangle(source=self.FOND_MENU_PATH, size=Window.size)
        )

        # Add button
        self.add_widget(
            Button(text="Menu", font_name=self.FONT_MENU_PATH, background_color=self.color_2,
                   pos_hint={'x': 0.82, 'y': 0}, size_hint=(0.18, 0.15),
                   on_press=self.switch_to_menu_screen)
        )

        menu_level_grid = GridLayout(size_hint=(0.7, 0.45), pos_hint={'x': 0.15, 'y': 0.3}, row=2)
        self.add_widget(menu_level_grid)

        set_list = os.listdir(self.MAPS_PATH)
        set_number = len(set_list)
        menu_level_grid.cols = set_number / 2

        for index in range(1, set_number + 1):
            if index % 2 == 0:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(
                        text=button_title,
                        font_name=self.FONT_MENU_PATH,
                        background_color=self.color_1,
                        on_press=self.launch_level,
                        cls=[index]
                    )
                )

            else:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(
                        text=button_title,
                        font_name=self.FONT_MENU_PATH,
                        background_color=self.color_2,
                        on_press=self.launch_level,
                        cls=[index]
                    )
                )

    def switch_to_menu_screen(self, *_):
        """
        Required method.
        """
        Logger.info("Propagate Menu")
        propagate_event('Menu', self)

    def launch_level(self, value):
        """
        Load level.
        :param value:
        :rtype: void
        """
        set_id = value.cls[0]
        if self.level_service.can_load_set(set_id):
            propagate_event('LevelManager', self, set_id)
        else:
            open_pop_up(self, 'not_unlocked', set_id)
