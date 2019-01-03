# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : pagination.py
# @Time    : 18-12-27 上午11:34
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from app.config import CONFIG


class BasePage:
    page_query_param = 'page'
    page_size = CONFIG.PAGE_SIZE

    def __init__(self, request, query):
        self.request = request
        self.query = query

    async def get_page(self):
        page = int(self.request.raw_args.get(self.page_query_param, 1))
        return page

    async def get_results(self):
        results = await self.request.app.db.execute(self.query.paginate(await self.get_page(), self.page_size))
        return [_._data for _ in results]

    async def total_count(self):
        return await self.request.app.db.count(self.query)

    @property
    async def data(self):
        return {
            'results': await self.get_results(),
            'count': await self.total_count(),
            'page': await self.get_page()
        }


class VideoPage(BasePage):
    page_size = 12
