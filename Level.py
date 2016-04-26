from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point
from MapCanvas import MapCanvas


class Level(FloatLayout):
    def __init__(self, map_file_path, textures, authorizations, **kwargs):
        """
        Load map in a layout and load level and touch properties.
        :param map_file_path: path to the map
        :param textures: textures dictionnary
        :param authorizations: authorizations dictionnary
        :param kwargs: layout's args
        """
        # load map
        super(Level, self).__init__(**kwargs)
        self.map_canvas = MapCanvas(map_file_path, textures)
        self.add_widget(self.map_canvas)

        # Load tile and touch properties.
        self.touch_width = int
        self.touch_scaling_factor = 6

        self.level_size = list
        self.tile_size = list

        self.x_max = int
        self.y_max = int
        self.touch_matrix = None

        self.color = (1, 1, 1)
        self.old_point = list
        self.point = list
        self.tile_identifier = list
        self.old_tile_identifier = list

        self.define_level_properties()

        # Load level victory path and authorizations.
        self.player_path = []
        self.win_path = []
        self.define_win_conditions()
        self.authorizations = authorizations

    ####
    # level properties for initialisation
    ####

    def define_level_properties(self):
        """
        :rtype: void
        """
        # Define touch width.
        self.touch_width = self.map_canvas.tile_size / self.touch_scaling_factor

        # Define real tile size.
        self.level_size = [self.map_canvas.window.size[0] - self.map_canvas.vectical_padding * 2,
                           self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding * 2]
        self.tile_size = [self.level_size[0] / self.map_canvas.map_size[0],
                          self.level_size[1] / self.map_canvas.map_size[1]]

        # Initialise matrix.
        self.x_max = self.map_canvas.map_size[0]
        self.y_max = self.map_canvas.map_size[1]
        self.touch_matrix = [[0 for _ in xrange(self.x_max)] for _ in xrange(self.y_max)]

        # Fill matrix.
        x = self.map_canvas.vectical_padding
        y = self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding
        for index_y in range(self.y_max):
            for index_x in range(self.x_max):
                self.touch_matrix[index_y][index_x] = [x, y, x + self.tile_size[0], y - self.tile_size[1]]
                x += self.tile_size[0]
            y -= self.tile_size[1]
            x = self.map_canvas.vectical_padding

    ####
    # Tiles and auth methods
    ####

    def get_tile(self):
        """
        get the current tile
        :rtype: tuple
        """
        for index_y in range(self.y_max):
            for index_x in range(self.x_max):
                horizontal_location = self.touch_matrix[index_y][index_x][0] <= self.point[0] < self.touch_matrix[index_y][index_x][2]
                vertical_location = self.touch_matrix[index_y][index_x][1] >= self.point[1] > self.touch_matrix[index_y][index_x][3]
                if horizontal_location and vertical_location:
                    return [index_y, index_x]
        return None

    def get_tile_properties(self, tile_identifier):
        """
        Find the current tile properties.
        :param tile_identifier: the tile number
        :rtype: boolean list of authorization or False if tile_type is not valid
        """

        if tile_identifier is None:
            return False

        tile_type = self.map_canvas.map_matrix[tile_identifier[0]][tile_identifier[1]]['type']
        tile_properties = self.authorizations[tile_type]
        if tile_type is None:
            raise Exception("Tile didn't get properties")

        return tile_properties

    def get_touch_direction(self):
        """
        get the touch direction
        :return: touch direction (integer)
        """
        y = self.tile_identifier[0]
        x = self.tile_identifier[1]
        y_old = self.old_tile_identifier[0]
        x_old = self.old_tile_identifier[1]

        if y > y_old: #bottom
            return 3
        elif y < y_old: #top
            return 2
        elif x > x_old: #right
            return 1
        elif x < x_old: #left
            return 0

        raise Exception("no direction provided")

    def can_start(self, tile_type):
        """
        test if player can start is path
        :param tile_type: string key of the texture
        :rtype: boolean
        """
        if tile_type == "W" or tile_type == "pading":
            return False
        return True

    def is_authorised(self, tile_authorization, direction):
        """
        Test the current tile to get authorizations.
        :param tile_authorization: boolean list of authorization {left, right, top, bot, start/stop}
        :param direction: (integer) direction of the tile
        :rtype: boolean
        """

        if type(tile_authorization) is not list:
            return False
        return tile_authorization[direction]


    ####
    # win methods
    ####

    def define_win_conditions(self):
        """
        Get win path and conditions.
        :type: void
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

    ####
    # Touch methods
    ####

    def on_touch_down(self, touch):

        # Save touch.
        ud = touch.ud
        ud['identifier'] = str(touch.uid)
        self.point = [touch.x, touch.y]
        self.player_path = []

        # Draw a point if player get authorisation.
        self.tile_identifier = self.get_tile()
        tile_type = self.get_tile_properties(self.tile_identifier)
        if self.can_start(tile_type):
            with self.canvas:
                Color(self.color)
                ud['points'] = [Point(points=self.point, pointsize=self.touch_width, group=ud['identifier'])]
        else:
            touch.ungrab(self)
            self.canvas.remove_group(ud['identifier'])
            return

        # Save coordinates.
        self.old_point = ud['points'][0].points[:]
        self.point = ud['points'][0].points[:]
        self.old_tile_identifier = self.tile_identifier[:]
        self.player_path.append([self.tile_identifier[0], self.tile_identifier[1]])

        # Launch touch.
        touch.grab(self)

    def on_touch_move(self, touch):

        # If touch launch.
        if touch.grab_current is not self:
            return

        # Save touch.
        ud = touch.ud
        ud['identifier'] = str(touch.uid)
        self.point = [touch.x, touch.y]

        # if change tile event
        self.tile_identifier = self.get_tile()
        if self.tile_identifier is None:
            is_authorised = False
        elif self.tile_identifier != self.old_tile_identifier:
            tile_properties = self.get_tile_properties(self.old_tile_identifier)
            direction = self.get_touch_direction()
            is_authorised = self.is_authorised(tile_properties, direction)
            if is_authorised:
                if [self.tile_identifier[0], self.tile_identifier[1]] in self.player_path:
                    is_authorised = False
                self.player_path.append([self.tile_identifier[0], self.tile_identifier[1]])
                print(self.player_path)
        else :
            is_authorised = True

        # Draw a point if player get authorisation.
        if is_authorised:
            with self.canvas:
                Color(self.color)
                ud['points'] = [Point(points=self.point, pointsize=self.touch_width, group=ud['identifier'])]
        else:
            touch.ungrab(self)
            self.canvas.remove_group(ud['identifier'])
            return

        # Save coordinates.
        self.old_point = [touch.x, touch.y]
        self.old_tile_identifier = self.tile_identifier

    def on_touch_up(self, touch):

        # If touch launch.
        if touch.grab_current is not self:
            return

        # If player win.
        self.tile_identifier = self.get_tile()
        tile_type = self.get_tile_properties(self.tile_identifier)
        if self.can_start(tile_type):
            if self.is_path_correct():
                print self.player_path
                # player win, need menu and other impl to finish
                return

        # Delete touch if loose.
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['identifier'])
        # player loose, need menu and other impl to finish
