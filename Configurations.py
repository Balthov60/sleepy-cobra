from kivy.uix.image import Image as CoreImage

import os.path

sources = {
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
    'point': './resources/other/point.png',
    'block': './resources/other/block.png',
    'trace': './resources/other/trace.png'
}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

# textures dictionary, format : textures path
textures = dict([
    ('trace', CoreImage(source=sources['trace']).texture),
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

# colos dictionary
color = dict([
    ('blue_color', [0.37, 0.69, 0.73, 0.9]),
    ('dark_blue_color', [0.19, 0.19, 0.19, 0.9])
])

# messages dictionary
messages = dict([
    ('11', "Welcome on 'Scape me !"
           "\n"
           "\nThe rules are really simple,"
           "\nYou must draw a line"
           "\nfrom a point to an other."
           "\nTo win, you need to go on all the case,"
           "\nbut don't go outside of the level !"
           "\n"
           "\nGood luck !"),
    ('12', "I think you've understand the game !"
           "\n"
           "\nWell, now i must told you,"
           "\nif you stop before"
           "\nyou complete all the set,"
           "\nyou will be force to replay"
           "\nall the levels of this set"
           "\nso take care !"
           "\n"
           "\nI really want to see this !"),
    ('21', "Nice, you are pretty good !"
           "\n"
           "\nBut it will be harder now,"
           "\nYou saw these black squares ?"
           "\ndon't touch them !"
           "\nwhy ? ahah Try ! you will see !"
           "\n"
           "\nGood luck !"),
    ('22', "Good !"
           "\n"
           "\nNow as for the first set,"
           "\nYou must finish all of this !"
           "\n"
           "\nI will pray for you !"),
    ('25', "God !"
           "\n"
           "\nThis one is not an easy one"
           "\nbut you could make it"
           "\n"
           "\nlet's go !"),
    ('23', "What this ? Something new ?"
           "\n"
           "\nYou can start where you want !"
           "\nand of course stop where you want."
           "\nbut the rules doesn't change"
           "\nyou must travel in all the case !"
           "\n"
           "\nI hope you will win this !"),
    ('31', "Wonderful !"
           "\n"
           "\nI hope that you wasn't thinking"
           "\nthat it was over !"
           "\nSo you see these white rectangles ?"
           "\nDon't forget what we say for the Square then !"
           "\n"
           "\nBe happy !"),
    ('32', "Ok it was an easy one !"
           "\n"
           "\nlet's continue !"),
    ('41', "Why those ***ing points always on the border ?"
           "\n"
           "\nOk let's try this, yeah ! better !"),
    ('51', "My mums always told me to set my sight highter "
           "\n"
           "\nNow I understand !"),
    ('52', "HARDER HARDER HARDER"),
    ('61', "Please don't cry I hate that !"),
    ('62', "\nAhahaha I love to see that"
           "\nYou know, I just need 2 minutes"
           "\nto make this level ^^"
           "\nand you ? to resolve it ?"
           "\n"
           "\nit's ok... it's ok move on..."),
    ('63', "I say DON'T CRY !!")
])

