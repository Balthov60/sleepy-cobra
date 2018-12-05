"""
LevelManager
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar
from kivy.properties import StringProperty
from kivy.lang import Builder

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher, propagate_event
from PopUpProvider import open_pop_up


class LevelManager(FloatLayout):
    """
    LevelManager children of FloatLayout.
    """

    def __init__(self, event_dispatcher, music_provider, **kwargs):
        """
        Instantiate the LevelManager with event listener.

        :param event_dispatcher: dispatcher
        :param kwargs:
        """
        super(LevelManager, self).__init__(**kwargs)
        self.size = Window.size
        self.event_dispatcher = event_dispatcher
        self.music_provider = music_provider
        self.level_service = LevelService()
        self.level_event_dispatcher = LevelEventDispatcher()
        self.popup = None
        self.current_set_id = int
        self.current_level_id_in_set = int
        self.level = None
        self.action_bar = None
        self.level_event_dispatcher.bind(on_level_completed=self.do_level_up)

    #####
    # Save and Level Up
    #####

    def do_level_up(self, _, completion_details, *unused):
        """
        Save level up in the completed pool and open popup.

        :param _:
        :param completion_details: Player stats.
        :param unused:
        :rtype: void
        """
        self.level_service.save_completion(completion_details)

        set_id_to_load = completion_details['set_id']
        level_id_in_set_to_load = completion_details['level_id_in_set'] + 1

        if level_id_in_set_to_load > 5:
            set_id_to_load = completion_details['set_id'] + 1
            level_id_in_set_to_load = 1

        open_pop_up(self, 'end_level', set_id_to_load, level_id_in_set_to_load, completion_details)

    #####
    # Set loading
    ####

    def load_level_in_set(self, set_id=None, level_id_in_set=1):
        """
        Load given level in given set with checking.

        :param set_id: id of the set to load.
        :param level_id_in_set: id of the level to load.
        :rtype: void
        """

        if not set_id or not self.level_service.does_set_exist(set_id):
            set_id = self.level_service.get_last_set_unlocked()

        self.clear_widgets()

        self.current_set_id = set_id
        self.current_level_id_in_set = level_id_in_set

        # display popup if level need popup
        open_pop_up(self, 'open_level', set_id, level_id_in_set)

        self.level = Level(
            self.level_event_dispatcher,
            set_id,
            level_id_in_set
        )
        self.add_widget(self.level)

        self.update_menu_level_bar()

        Window.bind(on_resize=self.update_menu_level_bar)

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

    def pop_up_menu(self, _):
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

    def update_menu_level_bar(self, *_):
        """
        Update the menu label of the level.

        :rtype: void
        """

        if not self.current_set_id or not self.current_level_id_in_set:
            return

        self.action_bar = Builder.load_file('LevelActionBar.kv')
        self.action_bar.current_level = 'Set: {0} - Level: {1}'.format(
            self.current_set_id, self.current_level_id_in_set
        )
        self.add_widget(self.action_bar)

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("Propagate Menu")
        propagate_event('MenuLevel', self)


class LevelActionBar(ActionBar):
    current_level = StringProperty()
