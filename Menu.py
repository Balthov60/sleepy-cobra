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

    def __init__(self, **kwargs):

        """
        Le menu.
        :param kwargs: Arguments du Layout
        """
        super(Menu, self).__init__(**kwargs)
        self.size=(300, 300)
        with self.canvas:
            Rectangle(source='resources/ArdoiseMenu.jpg',size=Window.size)

        button = Button(text="Jouer !",size_hint=(.45,.15),pos_hint={'x':.3, 'y':.4},on_press=self.do_something(1),
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
    def do_something(self, value):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        self.dispatch('on_test', value)


class Menu_level(FloatLayout):
    def __init__(self, **kwargs):
        super(Menu_level,self).__init__(self, **kwargs)


class MyEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_test')
        super(MyEventDispatcher, self).__init__(**kwargs)

    def on_test(self, *args):
        print "I am dispatched", args