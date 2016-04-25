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
        :rtype void
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
    # Tiles methods
    ####

    def is_authorised(self, tile_type):
        """
        Test the current tile to get authorizations.
        :param tile_type: string (key of the texture)
        :rtype boolean
        """
        if tile_type == "A":
            return True
        else:
            self.player_path = []
            return False

    def get_tile_properties(self):
        """
        Find the current tile properties.
        :rtype string (key of the texture)
        """
        for index_y in range(self.y_max):
            for index_x in range(self.x_max):
                horizontal_location = self.touch_matrix[index_y][index_x][0] <= self.point[0] < self.touch_matrix[index_y][index_x][2]
                vertical_location = self.touch_matrix[index_y][index_x][1] >= self.point[1] > self.touch_matrix[index_y][index_x][3]
                if horizontal_location and vertical_location:
                    tile_type = self.map_canvas.map_matrix[index_y][index_x]['type']
                    if tile_type is None:
                        raise Exception("Tile didn't get properties")
                    self.player_path.append([index_y, index_x])
                    return tile_type
        return "pading"

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
                if self.map_canvas.map_matrix[index_y][index_x]['type'] == 'A':
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
        tile_type = self.get_tile_properties()
        if self.is_authorised(tile_type):
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

        # Draw a point if player get authorisation.
        tile_type = self.get_tile_properties()
        if self.is_authorised(tile_type):
            with self.canvas:
                Color(self.color)
                ud['points'] = [Point(points=self.point, pointsize=self.touch_width, group=ud['identifier'])]
        else:
            touch.ungrab(self)
            self.canvas.remove_group(ud['identifier'])
            return

        # Save coordinates.
        self.old_point = [touch.x, touch.y]

    def on_touch_up(self, touch):

        # If touch launch.
        if touch.grab_current is not self:
            return

        # If player win.
        if self.is_path_correct():
            # player win, need menu and other impl to finish
            return

        # Delete touch if loose.
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['identifier'])
        # player loose, need menu and other impl to finish
