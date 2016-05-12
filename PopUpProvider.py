from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from Configurations import messages


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
    current_class.popup = None

    if state == 'Credits':
        create_raw_popup(current_class, 3, 3)

        add_popup_title(current_class, "Credits :")
        add_popup_credits(current_class)

        current_class.popup.open(current_class)

    elif state == 'not_unlocked':
        create_raw_popup(current_class)

        if add_unique_popup_message(current_class, state):
            current_class.popup.open(current_class)

    elif state == 'open_level':
        create_raw_popup(current_class)

        if add_unique_popup_message(current_class, state, set_id, level_id):
            current_class.popup.open(current_class)

    elif state == 'end_level':
        create_raw_popup(current_class, 3, 3)
        current_class.popup.auto_dismiss = False

        add_popup_title(current_class, "You won !")
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
    popup_size = window_size[0], window_size[1] / 2

    current_class.popup = ModalView(size_hint=(None, None), size=popup_size)
    current_class.grid_layout = GridLayout(cols=cols_quantity, raws=raws_quantity,
                                           row_default_height=popup_size[1] / (raws_quantity * 10),
                                           spacing=[popup_size[1] / 20, popup_size[1] / 10], padding=popup_size[0] / 25)

    current_class.popup.add_widget(current_class.grid_layout)


def add_popup_title(current_class, title_text=""):
    """
    Add Popup title.

    :param title_text:
    :param current_class:
    :rtype: void
    """
    current_class.grid_layout.add_widget(Label())
    current_class.grid_layout.add_widget(Label(text=title_text, font_size='40sp', color=(0, 0.6, 0.1, 1)))

    current_class.grid_layout.add_widget(Label())


def add_popup_infos_labels(current_class, completion_details):
    """
    Add attemps and time infos.

    :param current_class:
    :param completion_details:
    :rtype: void
    """
    time = completion_details['resolution_time']
    time = time.microseconds * 10**-6
    time_text = "Time\n" + str(time) + " sec."
    current_class.grid_layout.add_widget(Label(text=time_text, font_size='20sp'))

    current_class.grid_layout.add_widget(Label())

    attempts = completion_details['failed_attempts'] + 1
    attempts_text = "Attempts\n        " + str(attempts)
    current_class.grid_layout.add_widget(Label(text=attempts_text, font_size='20sp'))


def add_popup_buttons(current_class, set_id, level_id):
    """
    Add buttons Next, again and menu in pop up.

    :param current_class:
    :type level_id: object
    :param set_id:
    :rtype: void
    """
    again_button = Button(text='Play Again', cls=[set_id, level_id], background_color=(0.8, 0.5, 0, 1))
    again_button.bind(on_press=current_class.pop_up_replay)
    current_class.grid_layout.add_widget(again_button)

    menu_button = Button(text='Menu', background_color=(0, 0, 1, 1))
    menu_button.bind(on_press=current_class.pop_up_menu)
    current_class.grid_layout.add_widget(menu_button)

    next_button = Button(text='Next Level', cls=[set_id, level_id], background_color=(0, 0.6, 0.1, 1), size=[20, 20])
    next_button.bind(on_press=current_class.pop_up_next)
    current_class.grid_layout.add_widget(next_button)


def add_unique_popup_message(current_class, state, set_id=0, level_id=0):
    """

    :param level_id:
    :param set_id:
    :param current_class:
    :param state:
    :rtype: boolean
    """

    if state == 'not_unlocked':
        popup_label = Label(text="Level is not unlocked yet.", font_size='50sp', color=(0.8, 0.5, 0, 1))

    elif state == 'open_level':

        index = str(set_id) + str(level_id)
        if messages.get(index) is None:
            return False

        label_text = messages[index]
        popup_label = Label(text=label_text, font_size='15sp')

    else:
        raise Exception("State did not exist.")

    current_class.grid_layout.add_widget(popup_label)
    return True


def add_popup_credits(current_class):
    """

    :param current_class:
    :rtype: void
    """
    current_class.grid_layout.add_widget(Label())

    dev_text = "Devs : ISNABE corp'"
    current_class.grid_layout.add_widget(Label(text=dev_text, font_size='20sp', color=(0.8, 0, 0, 1)))

    for loop in range(2):
        current_class.grid_layout.add_widget(Label())

    music_text = "Music : M.Shvangiradze"
    current_class.grid_layout.add_widget(Label(text=music_text, font_size='20sp', color=(1, 0.5, 0, 1)))

