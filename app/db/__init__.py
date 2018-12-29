# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : __init__.py
# @Time    : 18-12-20 上午11:16
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

import aioredis
import peewee_async

from app.config import CONFIG

MYSQL_CONFIG = CONFIG.MYSQL
REDIS_CONFIG = CONFIG.REDIS

database = peewee_async.PooledMySQLDatabase(
    host=MYSQL_CONFIG['HOST'],
    port=int(MYSQL_CONFIG['PORT']),
    user=MYSQL_CONFIG['USER'],
    password=MYSQL_CONFIG['PASSWORD'],
    database=MYSQL_CONFIG['NAME'], charset='utf8mb4', autocommit=True)


async def init_db(app, loop):
    """
    Init db
    """
    app.db = peewee_async.Manager(database)
    app.db.connect()

    app.redis = await aioredis.create_pool(
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

    app.redis.close()
    await app.redis.wait_closed()


def create_table():
    """
    Create table
    """
    from app.db.models import (User, Token, Video, Task, Notice, Comment)

    User.create_table(True)
    Token.create_table(True)
    Video.create_table(True)
    Task.create_table(True)
    Notice.create_table(True)
    Comment.create_table(True)


if __name__ == '__main__':
    create_table()
