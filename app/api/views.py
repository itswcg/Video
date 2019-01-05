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
from app.api.serializers import UserSerializer, VideoSerializer, NoticeSerializer, TaskSerializer
from app.api.pagination import VideoPage, NoticePage, TaskPage

from app.db.models import (User, Token, Video, Task, Notice, Comment)

api_bp = Blueprint('api', url_prefix='/api')


class UserView(HTTPMethodView):

    @staticmethod
    @login_required()
    async def get(request, *args, **kwargs):
        user = request.app.user
        serializer = UserSerializer(request, user._data)
        results = await serializer.data

        return json(results, 200)

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
        """Get recommend or recent or single or all or search video"""
        data = request.raw_args
        if 'type' in data:
            if data['type'] == 'recommend':
                async with request.app.redis.get() as con:
                    recommend_videos = await con.execute('zrevrange', cs.REDIS_VIDEO_RECOMMEND, 0, 12)

                print(recommend_videos)

                query = Video.select().where(Video.id.in_(recommend_videos)).order_by(
                    Video.id.desc())  # Todo order_by list

                serializer = VideoSerializer(request, query, many=True)
                results = await serializer.data

                return json(results, 200)

            if data['type'] == 'recent':
                query = Video.select().order_by(Video.id.desc()).limit(12)

                serializer = VideoSerializer(request, query, many=True)
                results = await serializer.data

                return json(results, 200)

            if data['type'] == 'all':
                query = Video.select().order_by(Video.id.desc())

                page = VideoPage(request, query)
                serializer = VideoSerializer(request, await page.data, many=True)
                results = await serializer.data

                return json(results, 200)

        if 'video_id' in data:
            video = await request.app.db.get(Video, id=data['video_id'])

            serializer = VideoSerializer(request, video._data)
            results = await serializer.data

            async with request.app.redis.get() as con:
                await con.execute('incr', cs.REDIS_VIDEO_WATCH.format(data['video_id']))

            return json(results, 200)

        if 'search' in data:
            search_name = data.get('search')

            query = Video.select().where(Video.name.contains(search_name))

            page = VideoPage(request, query)
            serializer = VideoSerializer(request, await page.data, many=True)
            results = await serializer.data

            return json(results, 200)

        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)


class MyVideoView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        user = request.app.user

        query = Video.select().filter(user=user).order_by(Video.id.desc())

        page = VideoPage(request, query)
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

        serializer = VideoSerializer(request, video._data)
        results = await serializer.data

        return json(results, 200)


class TaskView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        user = request.app.user

        query = Task.select().filter(user=user).order_by(Task.is_complete)

        page = TaskPage(request, query)
        serializer = TaskSerializer(request, await page.data, many=True)
        results = await serializer.data

        return json(results, 200)

    async def post(self, request):
        user = request.app.user
        data = request.json

        if 'name' not in data:
            return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)

        await request.app.db.create(Task, user=user, name=data['name'])

        return json({cs.MSG_KEYWORD: cs.MSG_SUCCESS_DONE}, 200)


class NoticeView(HTTPMethodView):
    decorators = [login_required()]

    async def get(self, request):
        user = request.app.user

        query = Notice.select().filter(user=user).order_by(Notice.is_read)

        page = NoticePage(request, query)
        serializer = NoticeSerializer(request, await page.data, many=True)
        results = await serializer.data

        return json(results, 200)

    async def post(self, request):
        user = request.app.user
        data = request.json

        if 'type' in data:
            if data['type'] == 'single':
                notice_id = data.get('notice_id', 0)
                try:
                    notice = await request.app.db.get(Notice, id=notice_id)
                except Notice.DoesNotExist:
                    return json({cs.MSG_KEYWORD: cs.MSG_ERROR_NOTICE}, 400)
                else:
                    notice.is_read = 1
                    await request.app.db.update(notice)

                    return json({cs.MSG_KEYWORD: cs.MSG_SUCCESS_DONE}, 200)

            if data['type'] == 'all':
                notices = Notice.select().filter(user=user)
                for notice in notices:
                    notice.is_read = 1
                    await request.app.db.update(notice)

                return json({cs.MSG_KEYWORD: cs.MSG_SUCCESS_DONE}, 200)

        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)


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

        async with request.app.redis.get() as con:
            await con.execute('incr', cs.REDIS_VIDEO_COMMENT.format(data['video_id']))

        if user != video.user:
            await request.app.db.create(Notice,
                                        user=video.user,
                                        content=cs.MSG_NOTICE_COMMENT.format(user.username, video.name),
                                        notice_type=1,
                                        extra_data=video.video_url)

        return json({cs.MSG_KEYWORD: cs.MSG_SUCCESS_COMMENT}, 200)


async def like(request):
    data = request.json

    if 'video_id' not in data:
        return json({cs.MSG_KEYWORD: cs.MSG_ERROR_PARAMETER}, 400)

    try:
        video = await request.app.db.get(Video, id=data['video_id'])
    except Video.DoesNotExist:
        return json({cs.MSG_KEYWORD: cs.MSG_VIDEO_DELETE}, 200)
    else:
        async with request.app.redis.get() as con:
            likes = await con.execute('incr', cs.REDIS_VIDEO_LIKE.format(data['video_id']))

        await request.app.db.create(Notice,
                                    user=video.user,
                                    content=cs.MSG_NOTICE_LIKE,
                                    notice_type=2,
                                    extra_data=video.video_url)

        return json({'likes': likes}, 200)


api_bp.add_route(UserView.as_view(), '/user')
api_bp.add_route(VideoView.as_view(), '/video')
api_bp.add_route(MyVideoView.as_view(), '/my-video')
api_bp.add_route(TaskView.as_view(), '/task')
api_bp.add_route(NoticeView.as_view(), '/notice')
api_bp.add_route(comment, '/comment', methods=['POST'])
api_bp.add_route(like, '/like', methods=['POST'])
