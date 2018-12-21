# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : __init__.py
# @Time    : 18-12-20 上午11:16
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import aiomysql, aioredis
from sqlalchemy import create_engine, MetaData
from .models import (User, Token, Video, Task, Notice, Comment)
from app.config import CONFIG

MYSQL_CONFIG = CONFIG.MYSQL
REDIS_CONFIG = CONFIG.REDIS
MYSQL_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_CONFIG['USER'], MYSQL_CONFIG['PASSWORD'],
                                                    MYSQL_CONFIG['HOST'], MYSQL_CONFIG['PORT'], MYSQL_CONFIG['NAME'])


def create_table():
    """
    Create table
    """
    engine = create_engine(MYSQL_URI, isolation_level='AUTOCOMMIT')
    meta = MetaData()
    meta.create_all(bind=engine, tables=[User, Token, Video, Task, Notice, Comment])


async def init_db(app, loop):
    """
    Init db
    """
    app.db = await aiomysql.create_pool(
        host=MYSQL_CONFIG['HOST'],
        port=int(MYSQL_CONFIG['PORT']),
        user=MYSQL_CONFIG['USER'],
        password=MYSQL_CONFIG['PASSWORD'],
        db=MYSQL_CONFIG['NAME'], loop=loop, charset='utf8mb4', autocommit=True)

    app.redis_pool = await aioredis.create_pool(
        (REDIS_CONFIG['HOST'], REDIS_CONFIG['PORT']),
        db=int(REDIS_CONFIG['DB']),
        password=REDIS_CONFIG['PASSWORD'],
        minsize=5,
        maxsize=10,
        loop=loop
    )


async def close_db(app, loop):
    """
    Close db
    """
    app.db.close()
    await app.db.wait_closed()

    app.redis_pool.close()
    await app.redis_pool.wait_closed()


if __name__ == '__main__':
    create_table()
