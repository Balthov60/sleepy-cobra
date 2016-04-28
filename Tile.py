from Textures import authorizations


def get_tile_identifier(level, x, y):
    """
    Get the current tile identifier.

    :param level: Level class
    :param x: x from touch
    :param y: y from touch
    :return: tile identifier
    :rtype: list
    """

    for index_y in range(level.y_max):
        for index_x in range(level.x_max):
            horizontal_location_matches = \
                level.touch_matrix[index_y][index_x][0] <= x < level.touch_matrix[index_y][index_x][2]
            vertical_location_matches = \
                level.touch_matrix[index_y][index_x][1] >= y > level.touch_matrix[index_y][index_x][3]
            if horizontal_location_matches and vertical_location_matches:
                return index_y, index_x
    return None


def get_tile_properties(matrix, tile_identifier):
    """
    Get the current tile properties.

    :param matrix: tile matrix
    :param tile_identifier:
    :rtype: boolean list or False
    :return: authorizations of the current tile
    """

    tile_type = matrix[tile_identifier[0]][tile_identifier[1]]['type']
    if tile_type is None:
        raise Exception("Tile didn't get properties")

    return authorizations[tile_type]


def can_start_stop(tile_type, start_points, stop_points):
    """
    Test if player can start is path.

    :param tile_type: key of the texture (string)
    :rtype: boolean
    """
    if tile_type in start_points or tile_type in stop_points:
        return True

    return False


def is_authorised(level, tile_authorization, direction):
    """
    Test the current tile to get authorizations.

    :param level: Level class
    :param tile_authorization: boolean list of authorization {left, right, top, bot, start/stop}
    :param direction: direction of the tile (Integer)
    :rtype: boolean
    """

    if type(tile_authorization) is not list \
            or [level.tile_identifier[0], level.tile_identifier[1]] in level.player_path:
        return False

    return tile_authorization[direction]
