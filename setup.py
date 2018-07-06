from setuptools import setup, find_packages

setup(
    name='orb_catching_game',
    version='1.0',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    data_files=[('SETTINGS.json')],
    include_package_data=True,
    description='A game where a robot has to catch an orb in increasing difficult levels. Mean for RL purposes.',
    author='Andreas Verleysen'
)
