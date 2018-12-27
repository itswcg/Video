# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : serializers.py
# @Time    : 18-12-21 下午8:47
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import copy

from app.db.models import User, Token, Comment, Video


class BaseSerializer:
    fields = []

    def __init__(self, request, model, many=False):
        self.request = request
        self.model = model
        self.many = many

    @property
    async def data(self):
        if self.many:
            results, serializer_data = copy.deepcopy(self.model), []
            for result in results['results']:
                self.model, data = result, {}
                for field in self.fields:
                    data[field] = result.get(field, None)
                    if not data[field]:
                        data[field] = await getattr(self, field)()
                serializer_data.append(data)
            results['results'] = serializer_data
            return results

        else:
            data = {}
            for field in self.fields:
                data[field] = self.model.get(field, None)
                if not data[field]:
                    data[field] = await getattr(self, field)()
            return data


class UserSerializer(BaseSerializer):
    fields = ['username', 'avatar', 'phone', 'email', 'token']

    async def token(self):
        token, created = await self.request.app.db.get_or_create(Token, user_id=self.model['id'])
        return token.token


class VideoSerializer(BaseSerializer):
    fields = ['video_id', 'avatar', 'name', 'cover_url', 'video_url', 'create_time', 'comments', 'likes']

    async def video_id(self):
        return self.model['id']

    async def comments(self):
        comments = await self.request.app.db.execute(Comment.select().join(Video))

        return [_._data for _ in comments]

    async def likes(self):
        return ''

    async def avatar(self):
        user = await self.request.app.db.get(User, id=self.model['user'])
        return user.avatar


class CommentSerializer(BaseSerializer):
    fields = []
