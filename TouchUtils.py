from Configuration import authorizations


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


def get_touch_direction(tile_identifier, old_tile_identifier):
    """
    Get the simple touch direction. { 1 = bottom, 2 = top, 3 = right, 4 = left}

    :param old_tile_identifier: old tile coordinates
    :param tile_identifier: tile coordinates
    :return: simple touch direction
    :rtype: Integer
    """

    y = tile_identifier[0]
    x = tile_identifier[1]
    y_old = old_tile_identifier[0]
    x_old = old_tile_identifier[1]

    if y > y_old:
        return 3
    elif y < y_old:
        return 2
    elif x > x_old:
        return 1
    elif x < x_old:
        return 0

    raise Exception("No direction provided !")


def can_start_stop(tile_type, points_list):
    """
    Test if player can start is path.

    :param points_list: list of tile for start and stop
    :param tile_type: key of the texture (string)
    :rtype: boolean
    """
    if tile_type in points_list:
        return True

    return False


def is_authorised(tile_identifier, player_path, tile_authorization, direction):
    """
    Test the current tile to get authorizations.

    :param player_path:
    :param tile_identifier: tile coordinates
    :param level: Level class
    :param tile_authorization: boolean list of authorization {left, right, top, bot, start/stop}
    :param direction: direction of the tile (Integer)
    :rtype: boolean
    """

    if type(tile_authorization) is not list \
            or [tile_identifier[0], tile_identifier[1]] in player_path:
        return False

    return tile_authorization[direction]
