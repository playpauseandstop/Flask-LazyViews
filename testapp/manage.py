#!/usr/bin/env python

from flask.ext.script import Manager

from app import app


if __name__ == '__main__':
    Manager(app).run()
