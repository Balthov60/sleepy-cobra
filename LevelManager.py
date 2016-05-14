from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.button import Button, Label
from kivy.graphics import Color
from kivy.core.window import Window

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher, propagate_event
from PopUpProvider import open_pop_up


class LevelManager(Widget):
    popup = None
    grid_layout = None

    current_set_id = int
    current_level_id_in_set = int

    level = None
    current_level = None
    back_to_menu = None
    music= None

    def __init__(self, event_dispatcher, music_provider, **kwargs):
        """
        Instantiate the LevelManager with event listener.

        :param event_dispatcher: dispatcher
        :param kwargs:
        """
        super(LevelManager, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.music_provider = music_provider
        self.level_service = LevelService()
        self.level_event_dispatcher = LevelEventDispatcher()
        self.level_event_dispatcher.bind(on_level_completed=self.do_level_up)

    #####
    # Save and Level Up
    #####

    def do_level_up(self, instance, completion_details, *args):
        """
        Save level up in the completed pool and open popup.

        :param instance:
        :param completion_details:
        :param args:
        :rtype: void
        """
        self.level_service.save_completion(completion_details)

        set_id_to_load = completion_details['set_id']
        level_id_in_set_to_load = completion_details['level_id_in_set'] + 1

        if level_id_in_set_to_load >= 5:
            set_id_to_load = completion_details['set_id'] + 1
            level_id_in_set_to_load = 1

        open_pop_up(self, 'end_level', set_id_to_load, level_id_in_set_to_load, completion_details)

    #####
    # Set loading
    ####

    def load_level_in_set(self, set_id=None, level_id_in_set=1):
        """
        Load given level in given set with checking.

        :param set_id:
        :param level_id_in_set:
        :rtype: void
        """

        if not set_id or not self.level_service.does_set_exist(set_id):
            set_id = self.level_service.get_last_set_unlocked()

        self.clear_widgets()

        self.current_set_id = set_id
        self.current_level_id_in_set = level_id_in_set

        # add map
        self.level = self.add_widget(Level(self.level_event_dispatcher, set_id, level_id_in_set))

        self.update_menu_level_label()

        # display popup if level need popup
        open_pop_up(self, 'open_level', set_id, level_id_in_set)

        Window.bind(on_resize=self.update_menu_level_label)

    #####
    # Pop up
    #####

    def pop_up_next(self, instance):
        """
        When player click on next button in pop up.

        :param instance:
        :rtype: void
        """
        self.popup.dismiss()

        level_list = instance.cls
        self.load_level_in_set(level_list[0], level_list[1])

    def pop_up_replay(self, instance):
        """
        When player click on replay button in pop up.

        :param instance:
        :rtype: void
        """
        self.popup.dismiss()
        level_list = instance.cls
        if level_list[1] == 1:
            level_list[0] -= 1
            level_list[1] = 5
        else:
            level_list[1] -= 1

        self.load_level_in_set(level_list[0], level_list[1])

    def pop_up_menu(self, instance):
        """
        When player click on menu button in pop up.

        :param instance:
        :rtype: void
        """
        self.popup.dismiss()
        self.switch_to_menu_screen()

    #####
    # Menu relatives
    #####

    def update_menu_level_label(self, *args):
        """
        Update the menu label of the level.

        :rtype: void
        """

        self.size = Window.size

        if not self.current_set_id or not self.current_level_id_in_set:
            return

        self.remove_widget(self.current_level)
        self.remove_widget(self.back_to_menu)

        self.current_level = Label(
            text="Set: {0} - Level: {1}".format(self.current_set_id, self.current_level_id_in_set),
            size=(100, 20),
            pos=((Window.size[0] - 100) / 2, Window.size[1] * 14 / 15)
        )

        self.back_to_menu = Button(
            text="Menu",
            background_color=(0, 0, 0, 1),
            pos_hint=(0.1, 0.1),
            on_press=self.switch_to_menu_screen
        )

        self.music = Button(
            text="Music",
            background_color=(0, 0, 0, 1),
            pos=(0.9, 1),
            on_press=self.music_provider.update_sound_state
        )

        self.add_widget(self.current_level)
        self.add_widget(self.back_to_menu)
        self.add_widget(self.music)

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("Propagate Menu")
        propagate_event('Menu', self)
