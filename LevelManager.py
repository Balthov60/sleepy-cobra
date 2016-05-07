from kivy.uix.widget import Widget

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher


class LevelManager(Widget):

    def __init__(self, **kwargs):
        """
        Instantiate the LevelManager with event listener.
        :param kwargs:
        """
        super(LevelManager, self).__init__(**kwargs)
        self.level_service = LevelService()
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
        self.clear_widgets()
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

        if len(self.levels_completed_pool) > 5:
            self.levels_completed_pool = list()
            return

        if len(self.levels_completed_pool) < 5:
            return

        for level_completed in self.levels_completed_pool:
            self.level_service.save_completion(level_completed)

    def load_set(self, set_id=None):
        """
        Load level in set
        :param set_id:
        :return:
        """
        self.load_level_in_set(set_id)

    def load_level_in_set(self, set_id=None, level_id_in_set=1):
        """
        Load given level in given set with checking.
        :param set_id:
        :param level_id_in_set:
        :return:
        """

        if not self.level_service.does_set_exist(set_id) or not set_id:
                set_id = self.level_service.get_resuming_set()

        self.add_widget(Level(self.level_event_dispatcher, set_id, level_id_in_set))
