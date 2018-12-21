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


async def create_user(conn, nickName, passWord):
    """
    Create user
    """
    sql = User.insert().values(nickName=nickName, passWord=passWord)
    res = await trans(conn, sql)


async def get_user(conn, token):
    """
    Token to user
    """
    sql = Token.select()
