# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : migrations.py
# @Time    : 18-12-26 下午6:36
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from playhouse.migrate import *

from app.db import database

migrator = MySQLMigrator(database)

cover_url = CharField(verbose_name='cover_url', max_length=512, default='')

if __name__ == '__main__':
    migrate(
        migrator.add_column('video', 'cover_url', cover_url)
    )
