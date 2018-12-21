# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : models.py
# @Time    : 18-12-20 上午11:30
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import sqlalchemy as sa

metadata = sa.MetaData()

User = sa.Table('user', metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('nickName', sa.String(20)),
                sa.Column('avatarUrl', sa.String(512)),
                sa.Column('password', sa.String(218)),
                sa.Column('email', sa.String(52)),
                sa.Column('phone', sa.String(11)),
                sa.Column('createTime', sa.DateTime))

Token = sa.Table('token', metadata,
                 sa.Column('id', sa.Integer, primary_key=True))

Video = sa.Table('video', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('videoUrl', sa.String(512)),
                 sa.Column('createTime', sa.DateTime))

Task = sa.Table('task', metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('complete', sa.Boolean, default=False),
                sa.Column('createTime', sa.DateTime))

Notice = sa.Table('notice', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('createTime', sa.DateTime))

Comment = sa.Table('comment', metadata,
                   sa.Column('id', sa.Integer, primary_key=True))
