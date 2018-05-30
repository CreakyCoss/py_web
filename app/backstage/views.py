# -*- coding:UTF-8 -*-
from ..models import Role, User, Post, Comment
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose
import os
from .. import db, admin
from jinja2 import Markup
from ..functions import AccessControl
import datetime


class MyModelView(ModelView, AccessControl):
    pass


class MyFileAdmin(FileAdmin, AccessControl):
    pass


class UserView(MyModelView):

    # 搜索索引
    column_searchable_list = (User.email,)

    # 重命名列
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
        avatar_hash='头像',
        role='角色',
    )

    # 隐藏列
    column_exclude_list = (
        'about_me',
    )

    # 格式化列显示
    column_formatters = dict(
        # view, context, model, name
        password_hash=lambda v, c, m, p: '**' + m.password_hash[-6:],
        about_me=lambda v, c, m, p: m.about_me[:7] + '...' if m.about_me else '',
        avatar_hash=lambda v, c, m, p: Markup('<img src="%s">' % m.gravatar(size=32)),
        member_since=lambda v, c, m, p: Markup(
            "<script>document.write(moment('%s').format('LL'));</script>") % m.member_since,
        last_seen=lambda v, c, m, p: Markup(
            "<script>document.write(moment('%s').format('LL'));</script>") % m.last_seen,

    )


class RoleView(MyModelView):
    # 搜索索引
    column_searchable_list = (Role.name,)

    # 重命名列
    column_labels = dict(
        name='角色',
        default='默认',
        permissions='权限',
    )

    # 隐藏列
    column_exclude_list = (
        '',
    )

    # 格式化列显示
    column_formatters = dict(

    )


class PostView(MyModelView):

    # 搜索索引
    column_searchable_list = (Post.body,)

    # 重命名列
    column_labels = dict(
        body='文章内容',
        timestamp='发布时间',
        author='作者',
    )

    # 隐藏列
    column_exclude_list = (
        'body_html',
    )

    # 格式化列显示
    column_formatters = dict(
        body=lambda v, c, m, p: m.body[:100] + '...' if len(m.body) > 101 else m.body[:100],
        timestamp=lambda v, c, m, p: Markup(
            "<script>document.write(moment('%s').format('LLL'));</script>") % m.timestamp,
    )


class CommentView(MyModelView):
    # 搜索索引
    column_searchable_list = (Comment.body,)

    # 重命名列
    column_labels = dict(
        body='评论内容',
        timestamp='发布时间',
        disabled='屏蔽',
        author='评论者',
        post='评论文章',
    )

    # 隐藏列
    column_exclude_list = (
        'body_html',
    )

    # 格式化列显示
    column_formatters = dict(
        post=lambda v, c, m, p: (str(m.post))[0:50],
        timestamp=lambda v, c, m, p: Markup(
            "<script>document.write(moment('%s').format('LLL'));</script>") % m.timestamp,
    )


admin.add_view(UserView(User, db.session,  name='用户'))
admin.add_view(RoleView(Role, db.session, '角色'))
admin.add_view(PostView(Post, db.session, name='文章'))
admin.add_view(CommentView(Comment, db.session, '评论'))

basedir = os.path.dirname(os.path.dirname(__file__))
static_path = os.path.join(basedir, 'static')
admin.add_view(MyFileAdmin(static_path, '/static/', name='文件'))
