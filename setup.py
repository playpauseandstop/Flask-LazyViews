#!/usr/bin/env python

import os
import re
import sys

from setuptools import setup


DIRNAME = os.path.dirname(__file__)
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

with open(rel('README.rst')) as handler:
    README = handler.read()
with open(rel('flask_lazyviews', '__init__.py')) as handler:
    INIT_PY = handler.read()

INSTALL_REQUIRES = {
    2: ['Flask>=0.8'],
    3: ['Flask>=0.10.1'],
}
VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='Flask-LazyViews',
    version=VERSION,
    description='Registers URL routes for Flask application or blueprint in '
                'lazy way.',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='https://github.com/playpauseandstop/Flask-LazyViews',
    install_requires=INSTALL_REQUIRES[sys.version_info[0]],
    packages=[
        'flask_lazyviews',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='flask lazy views',
    license='BSD License',
)
