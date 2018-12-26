# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : models.py
# @Time    : 18-12-20 上午11:30
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import datetime

from app.config import CONFIG

from peewee import Model, CharField, DateTimeField, ForeignKeyField, BooleanField, IntegerField


class BaseModel(Model):
    create_time = DateTimeField(verbose_name='create_time', default=datetime.datetime.now)

    class Meta:
        from app.db import database
        database = database


class User(BaseModel):
    username = CharField(verbose_name='username', max_length=32, unique=True)
    password = CharField(verbose_name='password', max_length=512)
    avatar = CharField(verbose_name='avatar', max_length=512, default=CONFIG.DEFAULT_USER_AVATAR)
    email = CharField(verbose_name='email', max_length=52, null=True)
    phone = CharField(verbose_name='phone', max_length=11, null=True)


class Token(BaseModel):
    user_id = IntegerField(verbose_name='user_id', unique=True)
    token = CharField(verbose_name='token', max_length=512, unique=True)


class Video(BaseModel):
    user = ForeignKeyField(User, related_name='video')
    video_url = CharField(verbose_name='video_url', max_length=512)
    name = CharField(verbose_name='name', max_length=52)


class Task(BaseModel):
    user = ForeignKeyField(User, related_name='task')
    name = CharField(verbose_name='task', max_length=32)
    complete = BooleanField(verbose_name='complete', default=False)


class Notice(BaseModel):
    user = ForeignKeyField(User, related_name='notice')
    content = CharField(verbose_name='content', max_length=128)
    is_read = BooleanField(verbose_name='is_read', default=False)


class Comment(BaseModel):
    user = ForeignKeyField(User, related_name='comment')
    video = ForeignKeyField(Video, related_name='comment')
    content = CharField(verbose_name='content', max_length=1024)
