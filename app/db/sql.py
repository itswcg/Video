# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : sql.py
# @Time    : 18-12-20 下午2:45
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

# sql operation
from app.db.models import (User, Token, Video, Task, Notice, Comment)


async def trans(conn, sql):
    tran = await conn.begin
    try:
        res = await conn.execute(sql)
    except Exception:
        await tran.rollback()
    else:
        await conn.commit()
        return res


async def get_user_by_username(conn, username):
    pass


async def get_or_create_user(conn, username, password):
    """
    Create user
    """
    get_user = User.select().where()
    sql = User.insert().values(username=username, password=password)
    res = await trans(conn, sql)


async def get_user(conn, token):
    """
    Token to user
    """
    sql = Token.select().where(token == token)


async def update_user(conn, nickName, passWord):
    user = User.select().where(nickName == nickName)
    User.update().where(nickName=nickName).values(passWord=passWord)


async def delete_user(conn, nickName):
    User.delete().where(nickName == nickName)
