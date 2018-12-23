# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : models.py
# @Time    : 18-12-20 上午11:30
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import datetime

import sqlalchemy as sa

metadata = sa.MetaData()

User = sa.Table('user', metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('username', sa.String(20), index=True, nullable=False),
                sa.Column('password', sa.String(218), nullable=False),
                sa.Column('avatar', sa.String(512), default=''),
                sa.Column('email', sa.String(52), index=True),
                sa.Column('phone', sa.String(11), index=True),

                sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))

Token = sa.Table('token', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('user_id', sa.Integer, nullable=False),
                 sa.Column('token', sa.String(218), index=True, nullable=False),

                 sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))

Video = sa.Table('video', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('user_id', sa.Integer, index=True, nullable=False),
                 sa.Column('video_url', sa.String(512), nullable=False),
                 sa.Column('name', sa.String(52), nullable=False),

                 sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))

Task = sa.Table('task', metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('user_id', sa.Integer, index=True, nullable=False),
                sa.Column('name', sa.String(52), nullable=False),
                sa.Column('complete', sa.Boolean, default=False),

                sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))

Notice = sa.Table('notice', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('user_id', sa.Integer, index=True, nullable=False),
                  sa.Column('content', sa.String(128), nullable=False),
                  sa.Column('is_read', sa.Boolean, default=False),

                  sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))

Comment = sa.Table('comment', metadata,
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('user_id', sa.Integer, nullable=False),
                   sa.Column('video_id', sa.Integer, index=True, nullable=False),
                   sa.Column('content', sa.String(1024), nullable=False),

                   sa.Column('create_time', sa.DateTime, default=datetime.datetime.now()))
