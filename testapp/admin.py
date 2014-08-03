from flask.ext.admin import BaseView, expose


class AdminView(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin.html')
