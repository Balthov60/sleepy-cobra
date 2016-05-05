from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import os


class Menu(FloatLayout):
    FONT_MENU = 'resources/SIXTY.TTF'

    def __init__(self, event_dispatcher, **kwargs):
        """
        Initialize menu's button and textures.

        :param kwargs: Args of Layout
        :rtype: void
        """

        super(Menu, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher

        self.canvas.add(Rectangle(source='resources/test_im1.jpeg', size=Window.size))

        self.add_widget(Button(text="Jouer !", size_hint=(.45, .15), pos_hint={'x': .3, 'y': .4},
                               on_press=self.switch_to_menu_level_screen, font_name=self.FONT_MENU,
                               background_color=(0, 0, 0, 0), font_size='80sp'))

        self.add_widget(Button(text="Credits", size_hint=(.25, .1), pos_hint={'x': 0.4, 'y': 0.2},
                               font_name=self.FONT_MENU, background_color=(0, 0, 0, 0),
                               font_size='40sp'))

        self.add_widget(Button(text="Options", size_hint=(0.15, 0.12), pos_hint={'x': 0.85, 'y': 0},
                               font_name=self.FONT_MENU, background_color=(0, 0, 0, 0), font_size='25sp'))
        self.add_widget(Label(text="'Scape me", size_hint=(0.25, 0.1), pos_hint={'x': 0.37, 'y': 0.75},
                              font_name=self.FONT_MENU, font_size='100sp'))

    def propagate_event(self, value):
        """

        :param value: screen's name.
        :rtype: void
        """
        self.event_dispatcher.dispatch('on_change_screen', value)

    def switch_to_menu_level_screen(self, *args):
        """

        :param args:
        :rtype: void
        """
        self.propagate_event('Menu_level')


class MenuLevel(FloatLayout):
    FONT_MENU_LEVEL = 'resources/Eraser.ttf'

    def __init__(self, event_dispatcher, **kwargs):
        """
        Initialize button and textures of MenuLevel.

        :param event_dispatcher:
        :param kwargs: args of layout
        :rtype: void
        """
        super(MenuLevel, self).__init__(**kwargs)

        self.event_dispatcher = event_dispatcher

        def switch_to_menu_screen(*args):
            """

            :param args:
            :rtype: void
            """
            self.propagate_event('Menu')

        self.canvas.add(Rectangle(source='resources/test_im7.jpeg', size=Window.size))

        self.add_widget(Button(text="Back to Menu", pos_hint={'x': 0.82, 'y': 0}, size_hint=(0.18, 0.15),
                               font_name=self.FONT_MENU_LEVEL, on_press=switch_to_menu_screen,
                               background_color=(0.8, 0, 0, 0.85)))

        set_list = os.listdir('./resources/maps/')
        set_number = len(set_list)

        menu_level_grid = GridLayout(size_hint=(0.7, 0.45), pos_hint={'x': 0.15, 'y': 0.3}, row=2)
        self.add_widget(menu_level_grid)
        menu_level_grid.cols = set_number / 2

        for index in range(set_number):
            if index % 2 == 0:
                menu_level_grid.add_widget(Button(text="Level " + str(index + 1), background_color=(0.1, 0, 0, 0.85),
                                                  font_name=self.FONT_MENU_LEVEL))

            else:
                menu_level_grid.add_widget(Button(text="Level " + str(index + 1), background_color=(0.8, 0, 0, 0.85),
                                                  font_name=self.FONT_MENU_LEVEL))

    def propagate_event(self, value):
        """

        :param value: screen's name.
        :rtype: void
        """
        self.event_dispatcher.dispatch('on_change_screen', value)
