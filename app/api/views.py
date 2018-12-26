# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : views.py
# @Time    : 18-12-20 上午11:50
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg


from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import logger

from app.utils.decorator import login_required
from app.utils.functions import encrypt_password, generate_token
from app.api import constants as cs

from app.db.models import (User, Token, Video, Task, Notice, Comment)
from app.api.serializers import UserSerializer

api_bp = Blueprint('api', url_prefix='/api')


class UserView(HTTPMethodView):

    @staticmethod
    @login_required()
    async def get(request, *args, **kwargs):
        user = request.app.user

        return json(user)

    async def post(self, request):
        """login or create user"""
        data = request.json

        if 'username' not in data or 'password' not in data:
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)
        else:
            username = data['username']
            password = encrypt_password(data['password'])

            try:
                await request.app.db.get(User, username=username)
            except User.DoesNotExist:
                user = await request.app.db.create(User, username=username, password=password)
                token = generate_token()
                user_id = getattr(user, 'id')
                await request.app.db.create(Token, user_id=user_id, token=token)
            else:
                try:
                    user = await request.app.db.get(User, username=username, password=password)
                    user_id = getattr(user, 'id')
                except User.DoesNotExist:
                    return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PASSWORD}, 400)

            serializer = UserSerializer(user._data)

            token, created = await request.app.db.get_or_create(Token, user_id=user_id)

            results = serializer.data
            results['token'] = token.token
            return json(results, 200)

    @staticmethod
    @login_required()
    async def patch(request):
        """Patch user info"""
        user = request.app.user
        data = request.json
        keys = data.keys()

        allow_fields = ['password', 'avatar', 'email', 'phone']
        if any([_ not in allow_fields for _ in keys]):
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_FIELD}, 400)

        for field in keys:
            if field == 'password':
                password = encrypt_password(data.get(field))
                data[field] = password
            setattr(user, field, data.get(field))

        await request.app.db.update(user)
        serializer = UserSerializer(user._data)

        return json(serializer.data, 200)


class VideoView(HTTPMethodView):

    async def get(self, request, *args, **kwargs):
        """Get recommend or recent video"""
        data = request.raw_args
        if 'type' in data:
            if data['type'] == 'recommend':
                pass
            elif data['type'] == 'recent':
                pass

        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)


class MyVideoView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        pass

    async def post(self, request):
        pass


class TaskView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        pass

    async def post(self, request):
        pass


class NoticeView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        pass

    async def post(self, request):
        pass


@login_required()
async def comment(request):
    pass


@login_required()
async def like(request):
    pass


api_bp.add_route(UserView.as_view(), '/user')
api_bp.add_route(VideoView.as_view(), '/video')
api_bp.add_route(MyVideoView.as_view(), '/my-video')
api_bp.add_route(TaskView.as_view(), '/task')
api_bp.add_route(NoticeView.as_view(), '/notice')
api_bp.add_route(comment, '/comment', methods=['POST'])
api_bp.add_route(like, '/like', methods=['POST'])
