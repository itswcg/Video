# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : config.py
# @Time    : 18-12-20 上午11:11
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import os
from sys import path


class BaseConfig:
    """
    Base config of Video
    """
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path.append(PROJECT_DIR)
    DEFAULT_USER_AVATAR = 'http://blog.itswcg.com'
    SECRET_KEY = 'itswcg'
    DEBUG = True
    ACCESS_LOG = True
