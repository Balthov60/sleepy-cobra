from kivy.uix.image import Image as CoreImage
from kivy.graphics import Color

import os.path

sources = {
    'wall': 'resources/blocks/wall.png',
    'air': 'resources/blocks/air.png',
    'wall_left': 'resources/blocks/wall_left.png',
    'wall_right': 'resources/blocks/wall_right.png',
    'wall_top': 'resources/blocks/wall_top.png',
    'wall_bottom': 'resources/blocks/wall_bottom.png',
    'angle_left_bottom': 'resources/blocks/angle_left_bottom.png',
    'angle_left_top': 'resources/blocks/angle_left_top.png',
    'angle_right_bottom': 'resources/blocks/angle_right_bottom.png',
    'angle_right_top': 'resources/blocks/angle_right_top.png',
    'angle_top': 'resources/blocks/angle_top.png',
    'angle_bottom': 'resources/blocks/angle_bottom.png',
    'angle_right': 'resources/blocks/angle_right.png',
    'angle_left': 'resources/blocks/angle_left.png',
    'double_wall_horizontal': 'resources/blocks/double_wall_horizontal.png',
    'double_wall_vertical': 'resources/blocks/double_wall_vertical.png',
    'point': 'resources/other/point.png',
    'block': 'resources/other/block.png'
}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

# textures dictionary, format : textures path
textures = dict([
    ('block', CoreImage(source=sources['block']).texture),
    ('point', CoreImage(source=sources['point']).texture),
    ('W', CoreImage(source=sources['wall']).texture),
    ('A', CoreImage(source=sources['air']).texture),
    ('L', CoreImage(source=sources['wall_left']).texture),
    ('R', CoreImage(source=sources['wall_right']).texture),
    ('T', CoreImage(source=sources['wall_top']).texture),
    ('B', CoreImage(source=sources['wall_bottom']).texture),
    ('LB', CoreImage(source=sources['angle_left_bottom']).texture),
    ('LT', CoreImage(source=sources['angle_left_top']).texture),
    ('RB', CoreImage(source=sources['angle_right_bottom']).texture),
    ('RT', CoreImage(source=sources['angle_right_top']).texture),
    ('AT', CoreImage(source=sources['angle_top']).texture),
    ('AB', CoreImage(source=sources['angle_bottom']).texture),
    ('AR', CoreImage(source=sources['angle_right']).texture),
    ('AL', CoreImage(source=sources['angle_left']).texture),
    ('H', CoreImage(source=sources['double_wall_horizontal']).texture),
    ('V', CoreImage(source=sources['double_wall_vertical']).texture)
])

# authorization dictionary, format boolean list : {left, right, top, bot, start/stop}
authorizations = dict([
    ('W', [False, False, False, False]),
    ('A', [True, True, True, True]),
    ('L', [False, True, True, True]),
    ('R', [True, False, True, True]),
    ('T', [True, True, False, True]),
    ('B', [True, True, True, False]),
    ('LB', [False, True, True, False]),
    ('LT', [False, True, False, True]),
    ('RB', [True, False, True, False]),
    ('RT', [True, False, False, True]),
    ('AT', [False, False, False, True]),
    ('AB', [False, False, True, False]),
    ('AR', [True, False, False, False]),
    ('AL', [False, True, False, False]),
    ('H', [True, True, False, False]),
    ('V', [False, False, True, True]),
])

