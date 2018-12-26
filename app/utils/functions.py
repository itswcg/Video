# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : functions.py
# @Time    : 18-12-21 下午8:41
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import hashlib
import uuid
from app.config import CONFIG


def encrypt_password(pwd):
    hash = hashlib.md5()
    hash.update((pwd + CONFIG.SECRET_KEY).encode('utf-8'))
    return hash.hexdigest()


def generate_token():
    return uuid.uuid1()


if __name__ == '__main__':
    print(encrypt_password('wcg'))
