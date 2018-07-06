import json
import os.path

project_root = os.path.dirname(os.path.dirname(__file__))


def _get_computer_device_name():
    import platform
    return platform.node()


def dir_from_root(*paths, create=False):
    dir = os.path.join(project_root, *paths)
    if create: create_dir_if_not_exists(dir)
    return dir


def walk_path_with_extension(data_path, extension='jpg'):
    import fnmatch

    fragment_files = []
    for root, dirnames, filenames in os.walk(data_path):
        for filename in fnmatch.filter(filenames, '*.{}'.format(extension)):
            fragment_files.append(os.path.join(root, filename))

    return fragment_files


def create_dir_if_not_exists(*dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


def file_count_in(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])


def get_resource(resource_name: str):
    resource_dir = 'resources'
    return os.path.join(project_root, resource_dir, resource_name)


def remove_file_extension(filename):
    return '.'.join(filename.split('.')[:-1])


def settings():
    config_to_load = 'SETTINGS.json'
    with open(os.path.join(project_root, config_to_load)) as settings_file:
        settings = json.load(settings_file)

    return settings
