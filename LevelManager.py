from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.button import Button

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher, propagate_event


class LevelManager(Widget):

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
        self.levels_completed_pool = list()

    def add_widget(self, widget, index=0):
        """
        Add widget only after removing any widget previously present.
        :param widget:
        :param index:
        :return:
        """
        super(LevelManager, self).add_widget(widget, index)

    def do_level_up(self, instance, completion_details, *args):
        """
        Save advancement and level up the player loading next level.
        :param instance:
        :param completion_details:
        :param args:
        :return:
        """
        self.levels_completed_pool.append(completion_details)
        if completion_details['level_id_in_set'] >= 5:
            self.do_set_up()
            self.load_level_in_set()
            return

        self.load_level_in_set(completion_details['set_id'], completion_details['level_id_in_set'] + 1)

    def do_set_up(self):
        """

        :return:
        """

        if len(self.levels_completed_pool) > 5:
            self.levels_completed_pool = list()
            return

        if len(self.levels_completed_pool) < 5:
            return

        for level_completed in self.levels_completed_pool:
            self.level_service.save_completion(level_completed)

        self.levels_completed_pool = list()

    def load_set(self, set_id=None):
        """
        Load level in set
        :param set_id:
        :rtype: void
        """
        self.load_level_in_set(set_id)

    def can_load_set(self, set_id=None):
        """
        Test is player can play this set

        :param set_id:
        :rtype: Boolean
        """
        if not self.level_service.does_set_exist(set_id):
            Logger.info("Set does not exist.")
            return False

        if not self.level_service.is_set_unlocked(set_id):
            Logger.info("Level is not unlocked yet.")
            return False

        return True

    def load_level_in_set(self, set_id=None, level_id_in_set=1):
        """
        Load given level in given set with checking.
        :param set_id:
        :param level_id_in_set:
        :return:
        """

        if not set_id or not self.level_service.does_set_exist(set_id):
                set_id = self.level_service.get_resuming_set()

        self.clear_widgets()
        self.add_widget(Level(self.level_event_dispatcher, set_id, level_id_in_set))
        self.add_widget(
            Button(text="Menu", background_color=(0, 0, 0, 1), on_press=self.switch_to_menu_screen)
        )

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("propagate Menu")
        propagate_event('Menu', self)
