# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : __init__.py
# @Time    : 18-12-20 上午11:15
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import os


def load_config():
    """
    Load config
    """

    # mode = os.environ.get('MODE', 'DEV')
    mode = 'prod'
    try:
        if mode == 'prod':
            from .prod_config import ProdConfig
            return ProdConfig

        else:
            from .dev_config import DevConfig
            return DevConfig

    except ImportError:
        from .config import BaseConfig
        return BaseConfig


CONFIG = load_config()
