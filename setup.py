"""Based on: https://github.com/pypa/sampleproject."""

from setuptools import find_packages, setup
from os import path

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='board_game_store',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='Board game store management interface',
    long_description=long_description,

    url='https://github.com/tiagoshibata/board_game_store',

    author='Tiago Koji Castro Shibata',
    author_email='tiago.shibata@gmail.org',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='store database',

    packages=find_packages(),

    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['flask', 'Flask-Login', 'Flask-WTF', 'gevent', 'gunicorn', 'psycopg2'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        'board_game_store': [
            'static/*', 'templates/*.html', 'templates/*/*'
        ]
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
)
