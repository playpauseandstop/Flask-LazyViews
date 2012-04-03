from random import choice
from string import digits, letters

from flask import render_template


def home():
    query = u''.join([choice(letters + digits) for i in range(16)])
    return render_template('home.html', query=query)


def page(page_id):
    page = int(page_id)
    return render_template('page.html', page=page)
