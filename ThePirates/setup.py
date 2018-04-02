from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = [
    '*.tests',
    '*.tests.*',
    'tests.*',
    'tests',
]

INSTALL_REQUIRES = [
    'click==6.7',
    'Flask==0.12.2',
    'itsdangerous==0.24',
    'Jinja2==2.10',
    'MarkupSafe==1.0',
    'redis==2.10.6',
    'Werkzeug==0.14.1',
    'pymongo==3.6.1',
]

setup(
    name='the_pirates_ai',
    version='1.0',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    url='',
    license='',
    author='the pirates team',
    author_email='',
    description='Hackathon event',
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'competitor_list = hackathon.cli.export_log:do_competitor_list',
            'ship_place = hackathon.cli.export_log:do_ship_place',
            'shot_strategy = hackathon.cli.export_log:do_shoot_coordinate',
        ]
    },
)
