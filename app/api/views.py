# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : views.py
# @Time    : 18-12-20 上午11:50
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg


from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text, json
from sanic.log import logger

from app.db import sql

app = Sanic('some_name')


class UserView(HTTPMethodView):

    def get(self, request):
        return text('I am get method')

    def post(self, request):
        return text('I am post method')

    def put(self, request):
        return text('I am put method')

    def patch(self, request):
        return text('I am patch method')

    def delete(self, request):
        return text('I am delete method')


class Video(HTTPMethodView):

    def get(self, request):
        pass

    def post(self, request):
        pass
