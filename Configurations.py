"""
Configuration
"""
import os.path

from kivy.uix.image import Image as CoreImage


# SOURCES for maps textures.
SOURCES = {
    'wall': './resources/blocks/wall.png',
    'air': './resources/blocks/air.png',
    'wall_left': './resources/blocks/wall_left.png',
    'wall_right': './resources/blocks/wall_right.png',
    'wall_top': './resources/blocks/wall_top.png',
    'wall_bottom': './resources/blocks/wall_bottom.png',
    'angle_left_bottom': './resources/blocks/angle_left_bottom.png',
    'angle_left_top': './resources/blocks/angle_left_top.png',
    'angle_right_bottom': './resources/blocks/angle_right_bottom.png',
    'angle_right_top': './resources/blocks/angle_right_top.png',
    'angle_top': './resources/blocks/angle_top.png',
    'angle_bottom': './resources/blocks/angle_bottom.png',
    'angle_right': './resources/blocks/angle_right.png',
    'angle_left': './resources/blocks/angle_left.png',
    'double_wall_horizontal': './resources/blocks/double_wall_horizontal.png',
    'double_wall_vertical': './resources/blocks/double_wall_vertical.png',
    'block': './resources/blocks/block.png',
    'point': './resources/other/point.png',
    'trace': './resources/other/trace.png',
    'background': './resources/other/background_map_canvas.png'
}

for source_name in sorted(SOURCES):
    if not os.path.isfile(SOURCES[source_name]):
        raise ValueError("File %s does not exist." % SOURCES[source_name])

# Textures dictionary, format : (key, texture).
TEXTURES = dict([
    ('background', CoreImage(source=SOURCES['background']).texture),
    ('trace', CoreImage(source=SOURCES['trace']).texture),
    ('block', CoreImage(source=SOURCES['block']).texture),
    ('point', CoreImage(source=SOURCES['point']).texture),
    ('W', CoreImage(source=SOURCES['wall']).texture),
    ('A', CoreImage(source=SOURCES['air']).texture),
    ('L', CoreImage(source=SOURCES['wall_left']).texture),
    ('R', CoreImage(source=SOURCES['wall_right']).texture),
    ('T', CoreImage(source=SOURCES['wall_top']).texture),
    ('B', CoreImage(source=SOURCES['wall_bottom']).texture),
    ('LB', CoreImage(source=SOURCES['angle_left_bottom']).texture),
    ('LT', CoreImage(source=SOURCES['angle_left_top']).texture),
    ('RB', CoreImage(source=SOURCES['angle_right_bottom']).texture),
    ('RT', CoreImage(source=SOURCES['angle_right_top']).texture),
    ('AT', CoreImage(source=SOURCES['angle_top']).texture),
    ('AB', CoreImage(source=SOURCES['angle_bottom']).texture),
    ('AR', CoreImage(source=SOURCES['angle_right']).texture),
    ('AL', CoreImage(source=SOURCES['angle_left']).texture),
    ('H', CoreImage(source=SOURCES['double_wall_horizontal']).texture),
    ('V', CoreImage(source=SOURCES['double_wall_vertical']).texture)
])

# Authorization dictionary, format : boolean list {left, right, top, bot}
AUTHORIZATIONS = dict([
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

# Colors dictionary, format : (index, color). Color is R G B A / 360.
COLORS = dict([
    ('blue_color', [0.37, 0.69, 0.73, 0.9]),
    ('dark_blue_color', [0.19, 0.19, 0.19, 0.9])
])

# Messages dictionary, format : (index (level), string).
MESSAGES = dict([
    ('11', "Welcome on 'Scape me !"
           "\n"
           "\nThe rules are really simple,"
           "\nYou must draw a line"
           "\nfrom a point to an other."
           "\nTo win, you need to go through all squares,"
           "\nbut don't go outside of the level borders !"
           "\n"
           "\nGood luck !"),
    ('12', "I think you've got the idea !"
           "\n"
           "\nWell, I must told you"
           "\nif you stop before"
           "\nyou complete all levels from a set,"
           "\nyou will have to do it again."
           "\nThus be careful"
           "\n"
           "\nLet's go !"),
    ('21', "Nice, you're getting pretty good at this"
           "\n"
           "\nBut it's gonna get a bit harder from now on,"
           "\nYou saw these black squares ?"
           "\ndon't touch them !"
           "\nwhy ? ahah Try ! you will see !"
           "\n"
           "\nGood luck !"),
    ('22', "Good !"
           "\n"
           "\nNow like in the first set,"
           "\nYou must finish all of this !"
           "\n"
           "\nI will pray for you !"),
    ('25', "God !"
           "\n"
           "\nThis one is not an easy one"
           "\nbut you could make it"
           "\n"
           "\nLet's go !"),
    ('23', "What this ? Something new ?"
           "\n"
           "\nYou can start where you want !"
           "\nand of course stop where you want."
           "\nbut the rules don't change"
           "\nthrough all squares."
           "\n"
           "\nI hope you will achieve this one !"),
    ('31', "Wonderful !"
           "\n"
           "\nI hope you weren't thinking it's over..."
           "\nSo you see these white rectangles ?"
           "\nDon't forget what we said for the squares then !"
           "\n"
           "\nBe happy !"),
    ('32', "Ok it was an easy one !"
           "\n"
           "\nlet's continue !"),
    ('41', "Why those ****ing points always on the border ?"
           "\n"
           "\nOk let's try this, yeah ! better !"),
    ('51', "My mum always told me to look out of the box."
           "\n"
           "\nNow I understand !"),
    ('52', "HARDER HARDER HARDER"),
    ('61', "Please do not cry cry I hate that !"),
    ('62', "\nAhahaha I love to see that"
           "\nYou know, I just need 2 minutes"
           "\nto made this level ^^"
           "\nwhat about you ?"
           "\n"
           "\nit's ok... it's ok move on..."),
    ('63', "I said DO NOT CRY !!")
])
