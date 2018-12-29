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

from app.config import CONFIG

from app.utils.decorator import login_required
from app.utils.functions import encrypt_password, generate_token

from app.api import constants as cs
from app.api.serializers import UserSerializer, VideoSerializer
from app.api.pagination import BasePage

from app.db.models import (User, Token, Video, Task, Notice, Comment)

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
                except User.DoesNotExist:
                    return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PASSWORD}, 400)

            serializer = UserSerializer(request, user._data)
            results = await serializer.data

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
        serializer = UserSerializer(request, user._data)
        results = await serializer.data
        return json(results, 200)


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
        user = request.app.user

        query = Video.select().filter(user=user).order_by(Video.id.desc())

        page = BasePage(request, query)
        serializer = VideoSerializer(request, await page.data, many=True)
        results = await serializer.data

        return json(results, 200)

    async def post(self, request):
        user = request.app.user
        data = request.json

        if any([_ not in data for _ in ('name', 'video_url', 'cover_url')]):
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)

        video = await request.app.db.create(Video, user=user, name=data['name'], video_url=data['video_url'],
                                            cover_url=data['cover_url'])

        # serializer = VideoSerializer(video._data)
        print(video._data)
        return json({}, 200)


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
    user = request.app.user
    data = request.json

    if 'video_id' not in data or 'content' not in data:
        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)

    try:
        video = await request.app.db.get(Video, id=data['video_id'])
    except Video.DoesNotExist:
        return json({cs.MSG_KEYWORD: cs.MSG_VIDEO_DELETE}, 200)
    else:
        await request.app.db.create(Comment, user=user, video=video, content=data['content'])

        return json({cs.MSG_KEYWORD: cs.MSG_SUCCESS_COMMENT}, 200)


async def like(request):
    data = request.json

    if 'video_id' not in data:
        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)

    async with request.app.redis.get() as con:
        likes = await con.execute('incr', cs.REDIS_VIDEO_LIKE.format(data['video_id']))

    return json({'likes': likes}, 200)


api_bp.add_route(UserView.as_view(), '/user')
api_bp.add_route(VideoView.as_view(), '/video')
api_bp.add_route(MyVideoView.as_view(), '/my-video')
api_bp.add_route(TaskView.as_view(), '/task')
api_bp.add_route(NoticeView.as_view(), '/notice')
api_bp.add_route(comment, '/comment', methods=['POST'])
api_bp.add_route(like, '/like', methods=['POST'])
