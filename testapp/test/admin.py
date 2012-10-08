from flask import render_template
from flask.ext.admin import BaseView, expose


class AdminView(BaseView):

    @expose('/')
    def index():
        return render_template('admin/index.html')
