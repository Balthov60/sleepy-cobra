from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point
from MapCanvas import MapCanvas


class Level(FloatLayout):
    def __init__(self, map_file_path, textures, **kwargs):
        """
        Charge la carte dans un layout.
        :param map_file_path: Chemin de la carte
        :param textures: dictionnaire de textures
        :param kwargs: Argumens du layout
        """
        super(Level, self).__init__(**kwargs)
        self.map_canvas = MapCanvas(map_file_path, textures)
        self.tile_size = self.map_canvas.tile_size
        self.add_widget(self.map_canvas)

        self.touch_width = self.tile_size / 8

        self.origin_point = {0, 0}
        self.old_point = {0 , 0}
        self.point = {0, 0}

    def on_touch_down(self, touch):

        ud = touch.ud
        ud['identifier'] = str(touch.uid)

        with self.canvas:
            Color(0,0,1)
            ud['points'] = [Point(points=(touch.x, touch.y), pointsize=self.touch_width, group = ud['identifier'])]

        self.origin_point = ud['points'][-1].points[:]
        self.old_point = ud['points'][0].points[:]
        self.point = ud['points'][0].points[:]

        touch.grab(self)

    def on_touch_move(self, touch):

        if touch.grab_current is not self:
            return
        ud = touch.ud
        ud['identifier'] = str(touch.uid)

        x_dif = touch.x - self.old_point[0]
        y_dif = touch.y - self.old_point[1]

        if abs(x_dif) > abs(y_dif):
            self.point[0] = self.point[0] + x_dif
        else:
            self.point[1] = self.point[1] + y_dif
            print(self.old_point, "old")
            print(self.point, "point")
            print(self.origin_point, "origin")

        print(self.point, "point")

        with self.canvas:
            Color(0,0,1)
            ud['points'].append(
                Point(points=(self.point), pointsize=self.touch_width, group = ud['identifier']))

        self.old_point[0] = touch.x
        self.old_point[1] = touch.y

    def on_touch_up(self, touch):

        if touch.grab_current is not self:
            return
        touch.ungrab(self)

        ud = touch.ud
        self.canvas.remove_group(ud['identifier'])
