from setuptools import setup, find_packages

setup(
    name="advent_of_code",
    version="0.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        problems=aoc.scripts.problems:cli
    ''',
)
