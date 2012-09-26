#!/usr/bin/env python

import os

from distutils.core import setup


DIRNAME = os.path.dirname(__file__)

readme = open(os.path.join(DIRNAME, 'README.rst'), 'r')
README = readme.read()
readme.close()


setup(
    name='Flask-LazyViews',
    version='0.3',
    description='Registering url routes for Flask app and blueprints in ' \
                'lazy way.',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='https://github.com/playpauseandstop/Flask-LazyViews',
    install_requires=[
        'Flask',
    ],
    packages=[
        'flask_lazyviews',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='flask lazy views',
    license='BSD License',
)
