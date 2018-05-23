# -*- coding:UTF-8 -*-
from flask import Flask
from ..models import Permission, Role, User, Post, Comment
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os
import os
from .. import db, admin


# 后台管理页面的首页
class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class UserView(ModelView):
    column_searchable_list = (User.email,)  # 搜索索引
    column_labels = dict(
        email='邮箱',
        username='用户名',
        password_hash='密码',
        confirmed='认证',
        name='姓名',
        location='位置',
        about_me='自我描述',
        member_since='注册时间',
        last_seen='最后登陆时间',
        role='角色',
    )   # 重命名列
    column_exclude_list = (
        'avatar_hash',
    )   # 隐藏列
    column_formatters = dict(
        password_hash=lambda v, c, m, p: '**' + m.password_hash[-6:],
    )   # 格式化列显示


admin.add_view(UserView(User, db.session,  name='用户'))


admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))

basedir = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(basedir, 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

