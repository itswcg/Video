# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : decorator.py
# @Time    : 18-12-20 上午11:15
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from functools import wraps
from sanic.response import json


def check_request_for_authorization_status(request):
    pass


def login_required():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'detail': 'not_authorized'}, 403)

        return decorated_function

    return decorator
