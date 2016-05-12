from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Point

from MapCanvas import MapCanvas
from TouchUtils import get_tile_identifier, get_tile_properties, can_start_stop, is_authorised, get_touch_direction
from Configurations import authorizations, textures

from datetime import datetime


class Level(FloatLayout):
    """
    Touch methods and map utilisation with tiles implementation.
    """
    trace_texture = textures['trace']
    touch_scaling_factor = 6.5
    authorizations = authorizations

    def __init__(self, level_event_dispatcher, set_id, level_id_in_set, **kwargs):
        """
        Load map in a layout then load level and touch properties.

        :param level_event_dispatcher: Level Dispatcher.
        :param set_id: Current set's ID.
        :param level_id_in_set: Current level's ID.
        :param kwargs: layout's args.
        """
        super(Level, self).__init__(**kwargs)
        self.level_event_dispatcher = level_event_dispatcher

        # Load map in a canvas.
        self.set_id = set_id
        self.level_id_in_set = level_id_in_set
        map_file_path = "./resources/maps/set{0}/level{0}_{1}.cfg".format(self.set_id, self.level_id_in_set)

        self.map_canvas = MapCanvas(map_file_path)
        self.add_widget(self.map_canvas)

        # Initialize level variables.
        self.touch_width = int()

        self.level_size = list()
        self.tile_size = list()

        self.player_path = list()
        self.win_path = list()

        self.x_max = int()
        self.y_max = int()
        self.touch_matrix = None

        self.old_point = list()
        self.tile_identifier = list()
        self.old_tile_identifier = list()

        # Define level settings.
        self.define_level_properties()
        self.define_win_conditions()

        # Reset level stats.
        self.start_time = datetime.now()
        self.failed_attempts = 0

    ####
    # Touch methods.
    ####

    def on_touch_down(self, touch):
        """
        :param touch:
        :rtype: void
        """

        # Reset current path.
        self.player_path = []

        # get if player can draw here
        self.tile_identifier = get_tile_identifier(self, touch.x, touch.y)
        can_draw = can_start_stop(self.tile_identifier, self.map_canvas.points)

        if not can_draw:
            self.failed_attempts += 1
            self.canvas.after.clear()
            return

        self.canvas.after.add(
            Point(points=(touch.x, touch.y), texture=self.trace_texture, pointsize=self.touch_width)
        )

        # Save tile.
        self.old_tile_identifier = self.tile_identifier[:]
        self.player_path.append((self.tile_identifier[0], self.tile_identifier[1]))
        self.old_point = (touch.x, touch.y)

        touch.grab(self)

    def on_touch_move(self, touch):
        """
        :param touch:
        :rtype: void
        """

        if touch.grab_current is not self:
            return

        # get if player can draw (test if player is in a valid tile then test if tile change).
        self.tile_identifier = get_tile_identifier(self, touch.x, touch.y)
        if self.tile_identifier is None:
            can_draw = False

        elif self.tile_identifier != self.old_tile_identifier:
            old_tile_properties = get_tile_properties(self.map_canvas.map_matrix, self.old_tile_identifier)
            tile_properties = get_tile_properties(self.map_canvas.map_matrix, self.tile_identifier)
            direction = get_touch_direction(self.tile_identifier, self.old_tile_identifier)

            can_draw = is_authorised(self.tile_identifier, self.player_path,
                                     tile_properties, old_tile_properties, direction)
            if can_draw:
                self.player_path.append((self.tile_identifier[0], self.tile_identifier[1]))
        else:
            can_draw = True

        if not can_draw:
            self.failed_attempts += 1

            self.canvas.after.clear()
            touch.ungrab(self)
            return

        points_list = self.get_smooth_points(self.old_point[0], self.old_point[1], touch.x, touch.y)

        if not points_list:
            points_list = [(touch.x, touch.y)]

        for index in range(len(points_list)):
            x = points_list[index][0]
            y = points_list[index][1]
            self.canvas.after.add(
                Point(points=(x, y), texture=self.trace_texture, pointsize=self.touch_width)
            )

        # Save tile.
        self.old_tile_identifier = self.tile_identifier
        self.old_point = (touch.x, touch.y)

    def on_touch_up(self, touch):
        """
        :param touch:
        :rtype: void
        """

        if touch.grab_current is not self:
            return

        # get if player can draw here
        self.tile_identifier = get_tile_identifier(self, touch.x, touch.y)
        if self.tile_identifier is None:
            can_draw = False
        else:
            can_draw = can_start_stop(self.tile_identifier, self.map_canvas.points)

        if can_draw:
            if self.is_path_correct():
                return self.propagate_level_up()

        self.failed_attempts += 1

        # Delete touch if player loose.
        self.canvas.after.clear()
        touch.ungrab(self)
        return

    def get_smooth_points(self, x1, y1, x2, y2):
        """
        When player touch fast, get all the points between old and new point to smooth the trace.

        :param x1: new touch
        :param y1: new touch
        :param x2: old touch
        :param y2: old touch
        :return: List of tupples (coordinates for smooth points).
        """

        distance_x = x2 - x1
        distance_y = y2 - y1
        distance = (distance_x * distance_x + distance_y * distance_y) ** 0.5
        gap = self.touch_width / 4

        if distance < gap:
            return False

        points_list = list()
        quantity = distance / gap

        for index in range(1, int(quantity)):
            factor = index / quantity
            x = x1 + distance_x * factor
            y = y1 + distance_y * factor
            points_list.append((x, y))

        return points_list

    ####
    # Initialisation and level up.
    ####

    def define_level_properties(self):
        """
        Define properties for the current level.

        :rtype: void
        """

        self.touch_width = int(self.map_canvas.tile_size / self.touch_scaling_factor)

        # Define real tiles and level size.
        self.level_size = [self.map_canvas.window.size[0] - self.map_canvas.vertical_padding * 2,
                           self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding * 2]
        self.tile_size = [self.level_size[0] / self.map_canvas.map_size[0],
                          self.level_size[1] / self.map_canvas.map_size[1]]

        # Initialise then fill matrix.
        self.x_max = self.map_canvas.map_size[0]
        self.y_max = self.map_canvas.map_size[1]
        self.touch_matrix = []

        x = self.map_canvas.vertical_padding
        y = self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding

        for index_y in range(self.y_max):
            self.touch_matrix.append([])
            for index_x in range(self.x_max):
                self.touch_matrix[index_y].append((x, y, x + self.tile_size[0], y - self.tile_size[1]))
                x += self.tile_size[0]
            y -= self.tile_size[1]
            x = self.map_canvas.vertical_padding

    def propagate_level_up(self):
        """
        Propagate level_completed event.

        :rtype: void
        """

        self.level_event_dispatcher.dispatch('on_level_completed', {
            'set_id': self.set_id,
            'level_id_in_set': self.level_id_in_set,
            'resolution_time': datetime.now() - self.start_time,
            'failed_attempts': self.failed_attempts
        })

    ####
    # win methods
    ####

    def define_win_conditions(self):
        """
        Get win path.

        :rtype: void
        """
        for index_y in range(self.y_max):
            for index_x in range(self.x_max):
                if self.map_canvas.map_matrix[index_y][index_x]['type'] != 'W':
                    self.win_path.append((index_y, index_x))

    def is_path_correct(self):
        """
        Test if player win.

        :rtype: boolean
        """
        for entry in self.win_path:
            if entry not in self.player_path:
                self.failed_attempts += 1
                return False
            
        return True
