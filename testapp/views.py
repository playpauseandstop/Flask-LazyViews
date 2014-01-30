from random import choice, randint
from string import ascii_letters as letters, digits

from flask import render_template
from flask.views import MethodView
from sqlalchemy.exc import OperationalError

from models import Page


class PageView(MethodView):

    def get(self, page_id):
        return page(page_id)


def database_page(page_id=None):
    page_id = randint(1, 1024)

    try:
        page = Page.query.get(page_id)
    except OperationalError:
        page = Page(id=page_id,
                    title='Page #{0}'.format(page_id),
                    text='Dummy content.')

    return render_template('page.html', page=page.id)


def error(e):
    code = e.code if hasattr(e, 'code') else 500
    return (render_template('error.html', code=code, error=e), code)


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
    assert False, 'Hail to assertion error! Dummy is {0!r}'.format(DUMMY)
