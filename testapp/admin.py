from flask import render_template
from flask.ext.admin import BaseView, expose


class AdminView(BaseView):

    @expose('/')
    def index(self):
        return render_template('admin/index.html')
