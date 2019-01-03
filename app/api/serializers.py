# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : serializers.py
# @Time    : 18-12-21 下午8:47
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import copy

from app.db.models import User, Token, Comment, Video
from app.api import constants as cs


class BaseSerializer:
    fields = []

    def __init__(self, request, model, many=False):
        self.request = request
        self.model = model
        self.many = many

    async def get_data(self, res):
        self.model, data = res, {}
        for field in self.fields:
            data[field] = self.model.get(field, None)
            if data[field] is None:
                data[field] = await getattr(self, field)()

        return data

    @property
    async def data(self):
        if self.many:
            if 'results' in self.model:  # page serializer
                serializer_results, serializer_data = copy.deepcopy(self.model), []
                for res in serializer_results['results']:
                    data = await self.get_data(res)
                    serializer_data.append(data)
                serializer_results['results'] = serializer_data
                return serializer_results
            else:  # query serializer
                serializer_results = []
                for res in self.model:
                    data = await self.get_data(res._data)
                    serializer_results.append(data)
                return serializer_results

        else:  # get serializer
            return await self.get_data(self.model)


class UserSerializer(BaseSerializer):
    fields = ['username', 'avatar', 'phone', 'email', 'token']

    async def token(self):
        token, created = await self.request.app.db.get_or_create(Token, user_id=self.model['id'])
        return token.token


class VideoSerializer(BaseSerializer):
    fields = ['video_id', 'video_user', 'name', 'cover_url', 'video_url', 'create_time', 'comments', 'likes']

    async def video_id(self):
        return self.model['id']

    async def video_user(self):
        user = await self.request.app.db.get(User, id=self.model['user'])
        return {'username': user.username, 'avatar': user.avatar}

    async def comments(self):
        comments = await self.request.app.db.execute(Comment.select().join(Video).where(Video.id == self.model['id']))

        return [await CommentSerializer(self.request, _._data).data for _ in comments]

    async def likes(self):
        async with self.request.app.redis.get() as con:
            likes = await con.execute('get', cs.REDIS_VIDEO_LIKE.format(self.model['id']))
        return likes or '0'


class CommentSerializer(BaseSerializer):
    fields = ['comment_user', 'content', 'create_time']

    async def comment_user(self):
        user = await self.request.app.db.get(User, id=self.model['user'])
        return {'username': user.username, 'avatar': user.avatar}


class NoticeSerializer(BaseSerializer):
    fields = ['notice_id', 'content', 'is_read', 'create_time']

    async def notice_id(self):
        return self.model['id']


class TaskSerializer(BaseSerializer):
    fields = ['task_id', 'name', 'is_complete', 'create_time']

    async def task_id(self):
        return self.model['id']
