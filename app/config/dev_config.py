# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : dev_config.py
# @Time    : 18-12-20 上午11:25
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from .config import BaseConfig


class DevConfig(BaseConfig):
    SECRET_KEY = 'itswcgisdfkifd'
    MYSQL = {
        'NAME': 'video',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }

    REDIS = {
        'HOST': '127.0.0.1',
        'PORT': '6379',
        'PASSWORD': '',
        'DB': '0'
    }

    CELERY = {
        'CELERY_BROKER_URL': 'redis://localhost:6379/1',
        'CELERY_RESULT_BACKEND': 'redis://localhost:6379/1'
    }
