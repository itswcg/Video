# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : serializers.py
# @Time    : 18-12-21 下午8:47
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from app.db.models import Token


class BaseSerializer:

    def __init__(self, model):
        self.model = model

    @property
    def data(self):
        return


class UserSerializer(BaseSerializer):
    fields = ['avatar', 'phone', 'username', 'email']

    @property
    def data(self):
        data = {}
        for field in UserSerializer.fields:
            data[field] = self.model.get(field)
        return data
