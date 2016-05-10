from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher, propagate_event


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
        self.levels_completed_pool = list()

    def add_widget(self, widget, index=0):
        """
        Add widget only after removing any widget previously present.

        :param widget:
        :param index:
        :rtype: void
        """
        super(LevelManager, self).add_widget(widget, index)

    def do_level_up(self, instance, completion_details, *args):
        """
        Save level up and open popup.

        :param instance:
        :param completion_details:
        :param args:
        :return:
        """
        current_level_list = self.save_level_up(completion_details)
        self.open_pop_up(current_level_list[0], current_level_list[1], 'end_level', completion_details)

    def save_level_up(self, completion_details):
        """
        Save advancement.
        :param completion_details:
        :return: set_id, level_id (current)
        """
        self.levels_completed_pool.append(completion_details)
        if completion_details['level_id_in_set'] >= 5:
            set_id = self.do_set_up()
            return set_id, 1

        return completion_details['set_id'], completion_details['level_id_in_set'] + 1

    def do_set_up(self):
        """

        :return:
        """

        if len(self.levels_completed_pool) > 5:
            self.levels_completed_pool = list()
            return self.level_service.get_resuming_set()

        if len(self.levels_completed_pool) < 5:
            return self.level_service.get_resuming_set()

        for level_completed in self.levels_completed_pool:
            self.level_service.save_completion(level_completed)

        self.levels_completed_pool = list()
        return self.level_service.get_resuming_set()

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
        print(set_id, level_id_in_set)
        self.add_widget(Level(self.level_event_dispatcher, set_id, level_id_in_set))
        self.add_widget(
            Button(text="Menu", background_color=(0, 0, 0, 1), on_press=self.switch_to_menu_screen)
        )
        self.open_pop_up(set_id, level_id_in_set, 'open_level')
        self.update_level_label(set_id, level_id_in_set)

#####
# Pop Up
#####

    def open_pop_up(self, set_id, level_id, state, completion_details = None):
        """
        Try if this event need a pop up.

        :param completion_details:
        :param set_id:
        :param level_id:
        :param state: if player open or end a level
        :rtype: void
        """
        if state == 'open_level':
            return

        elif state == 'end_level':

            self.create_raw_popup()

            self.grid_layout.add_widget(Label())
            self.grid_layout.add_widget(Label(text="You win !"))

            self.add_infos_labels(completion_details)
            self.add_popup_buttons(set_id, level_id)

            self.popup.open()
        else:
            raise Exception("Pop up error.")

    def create_raw_popup(self):
        """
        Create a raw popup with windows size parameter.

        :rtype: void
        """
        window = self.get_parent_window()
        window_size = window.size
        popup_size = window_size[0] / 2, window_size[1] / 2
        self.popup = ModalView(size_hint=(None, None), size=popup_size)
        self.grid_layout = GridLayout(cols=3, raws=3,
                                      spacing=[0, popup_size[1] / 10], padding=popup_size[0] / 10)
        self.popup.add_widget(self.grid_layout)

    def add_popup_buttons(self, set_id, level_id):
        """
        Add buttons Next, again and menu in pop up.

        :rtype: void
        """
        again_button = Button(text='Play Again', cls=[set_id, level_id])
        again_button.bind(on_press=self.pop_up_replay)
        self.grid_layout.add_widget(again_button)

        menu_button = Button(text='Menu')
        menu_button.bind(on_press=self.pop_up_menu)
        self.grid_layout.add_widget(menu_button)

        next_button = Button(text='Next Level', cls=[set_id, level_id])
        next_button.bind(on_press=self.pop_up_next)
        self.grid_layout.add_widget(next_button)

    def add_infos_labels(self, completion_details):
        """
        Add attemps and time infos.

        :rtype: void
        """
        self.grid_layout.add_widget(Label())

        time = str(completion_details['resolution_time'])
        self.grid_layout.add_widget(Label(text="Time : " + time))

        self.grid_layout.add_widget(Label())

        attempts = str(completion_details['failed_attempts'])
        self.grid_layout.add_widget(Label(text="Attempts : " + attempts))

    def pop_up_next(self, instance):
        """
        When player click on next button in pop up.

        :param instance:
        :return:
        """
        level_list = instance.cls
        self.load_level_in_set(level_list[0], level_list[1])
        self.popup.dismiss()

    def pop_up_replay(self, instance):
        """
        When player click on replay button in pop up.

        :param instance:
        :return:
        """
        level_list = instance.cls
        if level_list[1] == 1:
            level_list[0] -= 1
            level_list[1] = 5
        else:
            level_list[1] -= 1

        self.load_level_in_set(level_list[0], level_list[1])
        self.popup.dismiss()

    def pop_up_menu(self, instance):
        """
        When player click on menu button in pop up.

        :param instance:
        :return:
        """
        self.popup.dismiss()
        self.switch_to_menu_screen()

#####
# Menu
#####

    def update_level_label(self, set_id, level_id_in_set):
        """
        Update the menu label of the level.

        :param set_id:
        :param level_id:
        :rtype: void
        """
        pass

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("propagate Menu")
        propagate_event('Menu', self)
