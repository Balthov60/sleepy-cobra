from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.button import Button

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher, propagate_event
from PopUpProvider import open_pop_up


class LevelManager(Widget):
    popup = None
    grid_layout = None

    def __init__(self, event_dispatcher, **kwargs):
        """
        Instantiate the LevelManager with event listener.

        :param event_dispatcher: dispatcher
        :param kwargs:
        """
        super(LevelManager, self).__init__(**kwargs)
        self.level_service = LevelService()
        self.event_dispatcher = event_dispatcher
        self.level_event_dispatcher = LevelEventDispatcher()
        self.level_event_dispatcher.bind(on_level_completed=self.do_level_up)

    def add_widget(self, widget, index=0):
        """
        Add widget only after removing any widget previously present.

        :param widget:
        :param index:
        :rtype: void
        """
        super(LevelManager, self).add_widget(widget, index)

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

    def can_load_set(self, set_id=None):
        """
        Test is player can play this set

        :param set_id:
        :rtype: Boolean
        """
        if not self.level_service.does_set_exist(set_id):
            raise Exception("Set does not exist.")

        if not self.level_service.is_set_unlocked(set_id):
            Logger.info("Level is not unlocked yet.")
            return False

        return True

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

        # add map
        self.add_widget(Level(self.level_event_dispatcher, set_id, level_id_in_set))

        # add menu level
        self.update_menu_level_label(set_id, level_id_in_set)

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

    def update_menu_level_label(self, set_id, level_id):
        """
        Update the menu label of the level.

        :param set_id:
        :param level_id:
        :rtype: void
        """
        self.add_widget(
            Button(text="Menu", background_color=(0, 0, 0, 1), on_press=self.switch_to_menu_screen)
        )

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("propagate Menu")
        propagate_event('Menu', self)
