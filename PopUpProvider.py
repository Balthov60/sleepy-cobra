from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


def open_pop_up(current_class, state, set_id=None, level_id=None, completion_details=None):
    """
    Try if this event need a pop up.

    :param current_class:
    :param completion_details:
    :param set_id:
    :param level_id:
    :param state: if player open or end a level
    :rtype: void
    """
    if state == 'not_unlocked':
        create_raw_popup(current_class)

        add_popup_error(current_class, state)

        current_class.popup.open(current_class)
    elif state == 'open_level':
        return
    elif state == 'end_level':
        create_raw_popup(current_class, 3, 3)

        add_popup_title(current_class)
        add_popup_infos_labels(current_class, completion_details)
        add_popup_buttons(current_class, set_id, level_id)

        current_class.popup.open(current_class)

    else:
        raise Exception("Pop up error.")


def create_raw_popup(current_class, cols_quantity=1, raws_quantity=1):
    """
    Create a raw popup with windows size parameter.

    :param raws_quantity:
    :param cols_quantity:
    :param current_class:
    :rtype: void
    """
    window = current_class.get_parent_window()
    window_size = window.size
    popup_size = window_size[0] / 2, window_size[1] / 2
    current_class.popup = ModalView(size_hint=(None, None), size=popup_size)
    current_class.grid_layout = GridLayout(cols=cols_quantity, raws=raws_quantity,
                                           spacing=[0, popup_size[1] / 10], padding=popup_size[0] / 10)
    current_class.popup.add_widget(current_class.grid_layout)


def add_popup_title(current_class):
    """
    Add Popup title.

    :param current_class:
    :rtype: void
    """
    current_class.grid_layout.add_widget(Label())
    current_class.grid_layout.add_widget(Label(text="You win !"))


def add_popup_infos_labels(current_class, completion_details):
    """
    Add attemps and time infos.

    :param current_class:
    :param completion_details:
    :rtype: void
    """
    current_class.grid_layout.add_widget(Label())

    time = completion_details['resolution_time']
    time = time.microseconds * 10**-6
    time_text = "Time : " + str(time) + " sec."
    current_class.grid_layout.add_widget(Label(text=time_text))

    current_class.grid_layout.add_widget(Label())

    attempts = completion_details['failed_attempts'] + 1
    attempts_text = "Attempts : " + str(attempts)
    current_class.grid_layout.add_widget(Label(text=attempts_text))


def add_popup_buttons(current_class, set_id, level_id):
    """
    Add buttons Next, again and menu in pop up.

    :param current_class:
    :type level_id: object
    :param set_id:
    :rtype: void
    """
    again_button = Button(text='Play Again', cls=[set_id, level_id])
    again_button.bind(on_press=current_class.pop_up_replay)
    current_class.grid_layout.add_widget(again_button)

    menu_button = Button(text='Menu')
    menu_button.bind(on_press=current_class.pop_up_menu)
    current_class.grid_layout.add_widget(menu_button)

    next_button = Button(text='Next Level', cls=[set_id, level_id])
    next_button.bind(on_press=current_class.pop_up_next)
    current_class.grid_layout.add_widget(next_button)


def add_popup_error(current_class, state):
    """

    :param current_class:
    :param state:
    :rtype: void
    """

    if state == 'not_unlocked':
        button = Button(text="Level is not unlocked yet.")
        button.bind(on_press=current_class.popup.dismiss)
        current_class.grid_layout.add_widget(button)

