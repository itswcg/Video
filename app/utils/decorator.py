# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : decorator.py
# @Time    : 18-12-20 上午11:15
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from functools import wraps
from sanic.response import json

from app.db.models import Token, User


async def check_request_for_authorization_status(request):
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
        if authorization[:5] == 'Token':
            token = authorization[6:]
            try:
                token_user = await request.app.db.get(Token, token=token)
                user_id = token_user._data['user_id']
                user = await request.app.db.get(User, id=user_id)
            except:
                pass
            else:
                request.app.user = user
                return True
    return False


def login_required():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            is_authorized = await check_request_for_authorization_status(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'detail': 'Not_authorized'}, 403)

        return decorated_function

    return decorator
