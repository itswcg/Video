# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : views.py
# @Time    : 18-12-20 上午11:50
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg


from sanic import Sanic, Blueprint
from sanic.views import HTTPMethodView
from sanic.response import text, json
from sanic.log import logger

from app.db import sql
from app.utils.decorator import login_required
from app.utils.functions import encrypt_password
from app.api import constants as cs

from app.db.models import (User, Token, Video, Task, Notice, Comment)

api_bp = Blueprint('api', url_prefix='/api')


class UserView(HTTPMethodView):

    @login_required()
    async def get(self, request):
        return text('I am get method')

    async def post(self, request):
        """login or create user"""
        data = request.json

        if 'username' not in data or 'password' not in data:
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)
        else:
            username = data['username']
            pwd = data['password']
            password = encrypt_password(pwd)

            user = await request.app.db.create(User, username=username, password=password)

            results = {'user': user}
            return json(results, 201)

    async def put(self, request):
        return text('I am put method')

    async def patch(self, request):
        return text('I am patch method')

    async def delete(self, request):
        return text('I am delete method')


class VideoView(HTTPMethodView):

    def get(self, request):
        pass

    def post(self, request):
        pass


api_bp.add_route(UserView.as_view(), '/user')
api_bp.add_route(VideoView.as_view(), '/video')
