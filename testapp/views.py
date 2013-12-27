from random import choice
from string import ascii_letters as letters, digits

from flask import render_template
from flask.views import MethodView


class PageView(MethodView):

    def get(self, page_id):
        return page(page_id)


def error(e):
    code = e.code if hasattr(e, 'code') else 500
    return render_template('error.html', code=code, error=e), code


def home():
    """
    Home page.
    """
    query = u''.join([choice(letters + digits) for i in range(16)])
    return render_template('home.html', query=query)


def page(page_id):
    page = int(page_id)
    return render_template('page.html', page=page)


def server_error():
    assert False, 'Hail to assertion error!'
