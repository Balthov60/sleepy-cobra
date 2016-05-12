from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger

from LevelService import LevelService
from LevelManager import LevelManager
from Configurations import color
from EventDispatchers import propagate_event
from PopUpProvider import open_pop_up

import os


class Menu(FloatLayout):
    FONT_MENU = './resources/menu/test19.ttf'

    def __init__(self, event_dispatcher, main, **kwargs):
        """
        Initialize menu's button and textures.

        :param event_dispatcher: dispatcher
        :param kwargs: Args of Layout
        :rtype: void
        """
        super(Menu, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.main = main

        # Add fond and title.
        self.canvas.add(
            Rectangle(source='./resources/menu/fondlogo.png', size=Window.size)
        )
        self.canvas.add(
            Rectangle(source='./resources/other/logo.png', size_hint=0.2, pos_hint={'x': 0.4, 'y': 0.4})
        )
        self.add_widget(
            Label(text="'Scape me", font_name=self.FONT_MENU, font_size='90sp',
                  size_hint=(0.25, 0.1), pos_hint={'x': 0.37, 'y': 0.75})
        )

        # Add buttons.
        self.add_widget(
            Button(text="Play !", font_name=self.FONT_MENU, font_size='80sp',
                   size_hint=(.45, .15), pos_hint={'x': .3, 'y': .4}, background_color=(0, 0, 0, 0),
                   on_press=self.switch_to_menu_level_screen)
        )

        self.add_widget(
            Button(text="Credits", font_name=self.FONT_MENU, font_size='40sp',
                   size_hint=(.25, .1), pos_hint={'x': 0.4, 'y': 0.2}, background_color=(0, 0, 0, 0),
                   on_press=self.credit_button_callback)
        )

        self.add_widget(
            Button(text="Music", font_name=self.FONT_MENU, font_size='25sp',
                   size_hint=(0.15, 0.12), pos_hint={'x': 0.85, 'y': 0}, background_color=(0, 0, 0, 0),
                   on_press=self.music_callback)
        )

    def switch_to_menu_level_screen(self, *args):
        """
        Required method.
        """
        Logger.info("Propagate MenuLevel")
        propagate_event('MenuLevel', self)

    def credit_button_callback(self, instance):
        """
        When player click on credit button (Required method).

        :param instance:
        :rtype: void
        """
        open_pop_up(self, 'Credits')

    def music_callback(self, instance):
        """
        Start/Stop music.

        :param instance:
        :rtype:
        """
        if self.main.sound.state == 'play':
            self.main.sound.stop()
            Logger.info("Music stop.")
        else:
            self.main.sound.play()
            Logger.info("Music start.")

class MenuLevel(FloatLayout):
    FONT_MENU_LEVEL = './resources/menu/test19.ttf'
    color_1 = color['blue_color']
    color_2 = color['dark_blue_color']

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
        self.level_manager = LevelManager(event_dispatcher)

        # Add fond.
        self.canvas.add(
            Rectangle(source='./resources/menu/fondlogo.png', size=Window.size)
        )

        # Add button
        self.add_widget(
            Button(text="Back to Menu", font_name=self.FONT_MENU_LEVEL, background_color=self.color_2,
                   pos_hint={'x': 0.82, 'y': 0}, size_hint=(0.18, 0.15),
                   on_press=self.switch_to_menu_screen)
        )

        menu_level_grid = GridLayout(size_hint=(0.7, 0.45), pos_hint={'x': 0.15, 'y': 0.3}, row=2)
        self.add_widget(menu_level_grid)

        set_list = os.listdir('./resources/maps/')
        set_number = len(set_list)
        menu_level_grid.cols = set_number / 2

        for index in range(1, set_number + 1):
            if index % 2 == 0:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(text=button_title, font_name=self.FONT_MENU_LEVEL,
                           background_color=self.color_1, on_press=self.launch_level, cls=[index])
                )

            else:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(text=button_title, font_name=self.FONT_MENU_LEVEL,
                           background_color=self.color_2, on_press=self.launch_level, cls=[index])
                )

    def switch_to_menu_screen(self, *args):
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
        if self.level_manager.can_load_set(set_id):
            propagate_event('LevelManager', self, set_id)
        else:
            open_pop_up(self, 'not_unlocked', set_id)
