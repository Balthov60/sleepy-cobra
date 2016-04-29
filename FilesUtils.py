import yaml
import os


def test_yaml_file(yaml_file_path):
    """
    Test if file exist and if file is valid.

    :param yaml_file_path:
    :rtype: void
    """

    is_file = os.path.isfile(yaml_file_path)
    if not is_file:
        raise ValueError("File given does not exist.")

    is_yaml = yaml_file_path.lower().endswith('.yaml')
    is_yml = yaml_file_path.lower().endswith('.yml')

    if not is_yaml and not is_yml:
        raise ValueError("File given is not valid for use.")


def test_cfg_file(map_file_path):
    """
    Test if file exist and if file is valid.

    :param map_file_path:
    :rtype: void
    """

    is_file = os.path.isfile(map_file_path)
    if not is_file:
        raise ValueError("File given does not exist.")

    is_cfg = map_file_path.lower().endswith('.cfg')

    if not is_cfg:
        raise ValueError("File given is not valid for use.")


def get_object_from_yaml(yaml_file_path, index_list):
    """
    Get the object in a YAML file.

    :param index_list:
    :param yaml_file_path:
    :return: the object of the yml file
    """

    try:
        yaml_file = open(yaml_file_path)
        yaml_content = yaml.load(yaml_file)

        if yaml_content is not None:
            if index_list[0] in yaml_content:
                value = yaml_content[index_list[0]]
                if index_list[1] in value:
                    return yaml_content[index_list[0]][index_list[1]]

        return None

    finally:
        yaml_file.close()


def set_object_in_yaml(yaml_file_path, index_list, value):
    """
    Set an object in a YAML file.

    :param value:
    :param index_list:
    :param yaml_file_path:
    :rtype: void
    """

    yaml_file = open(yaml_file_path)
    yaml_content = yaml.load(yaml_file)
    yaml_content[index_list[0]][index_list[1]] = value

    with open(yaml_file_path, "w") as f:
        yaml.dump(yaml_content, f)
