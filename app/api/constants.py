# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : constants.py
# @Time    : 18-12-21 下午9:43
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

MSG_KEYWORD = 'detail'

MSG_ERROR_PARAMETER = 'Parameter error'
MSG_ERROR_PASSWORD = 'Password error'
MSG_ERROR_FIELD = 'Field error'
MSG_ERROR_TASK = 'Task error'
MSG_ERROR_NOTICE = 'Notice error'

MSG_SUCCESS_COMMENT = '评论成功'
MSG_SUCCESS_DONE = '操作成功'

MSG_VIDEO_DELETE = '视频已被移除'
MSG_NOTICE_COMMENT = '{} 评论了你的视频：{}'
MSG_NOTICE_LIKE = '有人点赞了你的视频：{}'

REDIS_VIDEO_LIKE = 'video:{}:likes'
REDIS_VIDEO_WATCH = 'video:{}:watched'
REDIS_VIDEO_COMMENT = 'video:{}:comments'
REDIS_VIDEO_RECOMMEND = 'video:recommend_ranking'
