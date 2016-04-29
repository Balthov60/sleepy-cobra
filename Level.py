from kivy.uix.floatlayout import FloatLayout
from MapCanvas import MapCanvas
from kivy.graphics import Line, Color
from TouchUtils import get_tile_identifier, get_tile_properties, can_start_stop, is_authorised, get_touch_direction
from FilesUtils import set_object_in_yaml
from random import randint


class Level(FloatLayout):

    MAP = 'resources/maps/set'
    LEVEL = '/level'
    CFG = '.cfg'
    SEPARATOR = '_'
    ID = 'unique_identifier'
    SAVE_PATH = "resources/save.yml"

    def __init__(self, group, level, textures, authorizations, **kwargs):
        """
        Load map in a layout then load level and touch properties.

        :param map_file_path: path to the map
        :param textures: textures dictionnary
        :param authorizations: authorizations dictionnary
        :param kwargs: layout's args
        """

        # Defin global conditions.
        self.group = group
        self.level = level

        # Load map.
        self.textures = textures
        super(Level, self).__init__(**kwargs)
        map_file_path = "{0}{1}{2}{3}{4}{5}{6}".format(self.MAP, str(self.group), self.LEVEL, str(self.group),
                                                       self.SEPARATOR, str(self.level), self.CFG)
        self.map_canvas = MapCanvas(map_file_path, self.textures)
        self.add_widget(self.map_canvas)

        # Initialize variables.
        self.touch_width = int()
        self.touch_scaling_factor = 8

        self.level_size = list()
        self.tile_size = list()

        self.player_path = list()
        self.win_path = list()
        self.authorizations = authorizations

        self.x_max = int()
        self.y_max = int()
        self.touch_matrix = None

        self.old_point = list()
        self.tile_identifier = list()
        self.old_tile_identifier = list()

        # Define level settings.
        self.define_level_properties()
        self.define_win_conditions()

    ####
    # Touch methods
    ####

    def on_touch_down(self, touch):
        """
        :param touch:
        :rtype: void
        """

        # Save current touch.
        ud = touch.ud
        ud[self.ID] = str(touch.uid)
        self.player_path = []

        # get if player can draw here
        self.tile_identifier = get_tile_identifier(self, touch.x, touch.y)
        if self.tile_identifier is None:
            can_draw = False
        else:
            can_draw = can_start_stop(self.tile_identifier, self.map_canvas.points)

        if not can_draw:
            self.canvas.remove_group(ud[self.ID])
            return

        with self.canvas:
            Color(0.97, 0.97, 1)
            for diameter in range(1, self.touch_width):
                Line(circle=(touch.x, touch.y, diameter),
                     group=ud[self.ID])

        # Save tile.
        self.old_tile_identifier = self.tile_identifier[:]
        self.player_path.append([self.tile_identifier[0], self.tile_identifier[1]])
        self.old_point = [touch.x, touch.y]

        touch.grab(self)

    def on_touch_move(self, touch):
        """
        :param touch:
        :rtype: void
        """

        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud[self.ID] = str(touch.uid)

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
                self.player_path.append([self.tile_identifier[0], self.tile_identifier[1]])
        else:
            can_draw = True

        if not can_draw:
            touch.ungrab(self)
            self.canvas.remove_group(ud[self.ID])
            return

        points_list = self.get_smooth_points(self.old_point[0], self.old_point[1], touch.x, touch.y)

        if not points_list:
            points_list = [[touch.x, touch.y]]

        for index in range(len(points_list)):
            x = points_list[index][0]
            y = points_list[index][1]
            with self.canvas:
                gap = randint(1, 3)
                for diameter in range(1, self.touch_width, gap):
                        Line(circle=(x, y, diameter),
                             group=ud[self.ID])

        # Save tile.
        self.old_tile_identifier = self.tile_identifier
        self.old_point = [touch.x, touch.y]

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
            # Delete touch if player loose.
            if self.is_path_correct():
                self.level_up()

        ud = touch.ud
        touch.ungrab(self)
        self.canvas.remove_group(ud[self.ID])
        return

        # player win, need menu and other impl to finish

    def get_smooth_points(self, x1, y1, x2, y2):
        """
        When player touch fast, get all the points between old and new point to smooth the trace.

        :param x1: new touch
        :param y1: new touch
        :param x2: old touch
        :param y2: old touch
        :type: 2D list
        :return: list of coordinates for smooth points
        """

        dx = x2 - x1
        dy = y2 - y1
        distance = (dx * dx + dy * dy)**0.5
        gap = self.touch_width / 7

        if distance < gap:
            return False

        points_list = list()
        quantity = distance / gap

        for index in range(1, int(quantity)):
            factor = index / quantity
            x = x1 + dx * factor
            y = y1 + dy * factor
            points_list.append([x, y])

        return points_list

    ####
    # initialisation and level up
    ####

    def define_level_properties(self):
        """
        Define prperties for the current level.

        :rtype: void
        """

        self.touch_width = int(self.map_canvas.tile_size / self.touch_scaling_factor)

        # Define real tiles and level size.
        self.level_size = [self.map_canvas.window.size[0] - self.map_canvas.vectical_padding * 2,
                           self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding * 2]
        self.tile_size = [self.level_size[0] / self.map_canvas.map_size[0],
                          self.level_size[1] / self.map_canvas.map_size[1]]

        # Initialise then fill matrix.
        self.x_max = self.map_canvas.map_size[0]
        self.y_max = self.map_canvas.map_size[1]
        self.touch_matrix = [[0 for _ in xrange(self.x_max)] for _ in xrange(self.y_max)]

        x = self.map_canvas.vectical_padding
        y = self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding

        for index_y in range(self.y_max):
            for index_x in range(self.x_max):
                self.touch_matrix[index_y][index_x] = [x, y, x + self.tile_size[0], y - self.tile_size[1]]
                x += self.tile_size[0]
            y -= self.tile_size[1]
            x = self.map_canvas.vectical_padding

    def reset_old_properties(self):
        """
        Reset properties of the old level.

        :rtype: void
        """
        # Initialize variables.

        self.touch_matrix = None
        self.remove_widget(self.map_canvas)

        self.old_point = list()
        self.tile_identifier = list()
        self.old_tile_identifier = list()
        self.win_path = list()
        self.player_path = list()

    def level_up(self):
        """
        Load the next map canvas and properties/

        :rtype: void
        """

        self.level += 1
        if self.level > 5:
            self.group += 1
            set_object_in_yaml(self.SAVE_PATH, ['player_save', 'group'], self.group)
            self.level = 1

        set_object_in_yaml(self.SAVE_PATH, ['player_save', 'level'], self.level)

        map_file_path = "{0}{1}{2}{3}{4}{5}{6}".format(self.MAP, str(self.group), self.LEVEL, str(self.group),
                                                       self.SEPARATOR, str(self.level), self.CFG)

        self.reset_old_properties()

        self.map_canvas = MapCanvas(map_file_path, self.textures)
        self.add_widget(self.map_canvas)

        self.define_level_properties()
        self.define_win_conditions()

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
                    self.win_path.append([index_y, index_x])

    def is_path_correct(self):
        """
        Test if player win.

        :rtype: boolean
        """
        for entry in self.win_path:
            if entry not in self.player_path:
                return False
        return True
