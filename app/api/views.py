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
from app.utils.decorator import login_required
from app.utils.functions import encrypt_password
from app.api import constants as cs

app = Sanic('some_name')


class UserView(HTTPMethodView):

    @login_required()
    def get(self, request):
        return text('I am get method')

    def post(self, request):
        """login or create user"""
        data = request.json

        if 'username' not in data or 'password' not in data:
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)
        else:
            username = data['username']
            pwd = data['password']
            password = encrypt_password(pwd)

            with request.app.db.acquire() as conn:
                res = await sql.get_user_by_username(conn, username)
                if res:
                    return json({cs.MSG_KEYWORD: cs.MSG_ERROR_ALREADY_REGISTER}, 400)

            with request.app.db.acquire() as conn:
                await sql.get_or_create_user(conn, username, password)

            results = {}
            return json(results, 201)

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
