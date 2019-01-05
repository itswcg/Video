# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : models.py
# @Time    : 18-12-20 上午11:30
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import datetime

from app.config import CONFIG

from peewee import Model, CharField, DateTimeField, ForeignKeyField, IntegerField


class BaseModel(Model):
    create_time = DateTimeField(verbose_name='create_time', default=datetime.datetime.now)

    class Meta:
        from app.db import database
        database = database


class User(BaseModel):
    username = CharField(verbose_name='username', max_length=32, unique=True)
    password = CharField(verbose_name='password', max_length=512)
    avatar = CharField(verbose_name='avatar', max_length=512, default=CONFIG.DEFAULT_USER_AVATAR)
    email = CharField(verbose_name='email', max_length=52, default='')
    phone = CharField(verbose_name='phone', max_length=11, default='')


class Token(BaseModel):
    user_id = IntegerField(verbose_name='user_id', unique=True)
    token = CharField(verbose_name='token', max_length=512, unique=True)


class Video(BaseModel):
    user = ForeignKeyField(User, related_name='video')
    name = CharField(verbose_name='name', max_length=52)
    video_url = CharField(verbose_name='video_url', max_length=512)
    cover_url = CharField(verbose_name='cover_url', max_length=512)


class Task(BaseModel):
    user = ForeignKeyField(User, related_name='task')
    name = CharField(verbose_name='task', max_length=32)
    is_complete = IntegerField(verbose_name='is_complete', default=0)


class Notice(BaseModel):
    user = ForeignKeyField(User, related_name='notice')
    content = CharField(verbose_name='content', max_length=128)
    notice_type = IntegerField(verbose_name='notice_type', default=0, help_text='{0: 系统通知, 1: 视频评论, 2: 视频点赞}')
    extra_data = CharField(verbose_name='extra_data', max_length=512)
    is_read = IntegerField(verbose_name='is_read', default=0)


class Comment(BaseModel):
    user = ForeignKeyField(User, related_name='comment')
    video = ForeignKeyField(Video, related_name='comment')
    content = CharField(verbose_name='content', max_length=1024)
