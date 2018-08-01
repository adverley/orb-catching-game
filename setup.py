from setuptools import setup, find_packages


def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)])


setup(
    name='orb_catching_game',
    version='1.0',
    packages=create_package_list('orb_catching_game'),
    data_files=[('orb_catching_game/SETTINGS.json')],
    include_package_data=True,
    install_requires=[
        'pygame',
        'B'
    ],
    description='A game where a robot has to catch an orb in increasing difficult levels. Meant for RL purposes.',
    author='Andreas Verleysen'
)
