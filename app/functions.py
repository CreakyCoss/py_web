from flask_admin import AdminIndexView, expose, BaseView
from flask import redirect, abort, url_for, request, flash
from flask_login import current_user


class AccessControl(BaseView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.is_administrator():
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                flash("Please log in to access this page.")
                return redirect(url_for('auth.login', next=request.url))


class MyAdminIndexView(AdminIndexView, AccessControl):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')