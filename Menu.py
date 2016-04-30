from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy._event import EventDispatcher

class Menu(FloatLayout):

    def __init__(self,event_dispatcher, **kwargs):

        """
        Le menu.
        :param kwargs: Arguments du Layout
        """
        super(Menu, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.size=(300, 300)
        with self.canvas:
            Rectangle(source='resources/ArdoiseMenu.jpg',size=Window.size)

        def switch_to_menu_screen(*args):
            self.propagate_event('Menu_level')

        button = Button(text="Jouer !",size_hint=(.45,.15),pos_hint={'x':.3, 'y':.4},on_press=switch_to_menu_screen,
                                    font_name="resources/Eraser.ttf",background_color=(0,0,0,0), font_size="80sp")
        self.add_widget(button)

        btncredits = Button(text="Credits",size_hint=(.25,.1),pos_hint={'x':0.4, 'y':0.2},
            font_name="resources/Eraser.ttf",background_color=(0,0,0,0), font_size="40sp")
        self.add_widget(btncredits)

        btnoptions = Button(text="Options",size_hint=(0.15,0.12),pos_hint={'x':0.85, 'y':0},
            font_name="resources/Eraser.ttf",background_color=(0,0,0,0),font_size="25sp")
        self.add_widget(btnoptions)
        l = Label(text="'Scape me",size_hint=(0.25,0.1) ,pos_hint={"x":0.37,"y":0.7},
                                font_name="resources/Eraser.ttf",font_size="100sp")
        self.add_widget(l)

    def propagate_event(self,value):
        self.event_dispatcher.dispatch('on_change_screen', value)





class Menu_level(FloatLayout):
    def __init__(self,event_dispatcher, **kwargs):
        super(Menu_level,self).__init__( **kwargs)
