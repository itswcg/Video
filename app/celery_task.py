# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : celery.py
# @Time    : 19-1-4 下午2:49
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from celery import Celery
from celery.schedules import crontab

from app.config import CONFIG
from app.api import constants as cs
from app.db.models import Video
import redis  # celery use sync

REDIS_CONFIG = CONFIG.REDIS
pool = redis.ConnectionPool(host=REDIS_CONFIG['HOST'], port=REDIS_CONFIG['PORT'], db=REDIS_CONFIG['DB'],
                            password=REDIS_CONFIG['PASSWORD'])
con = redis.Redis(connection_pool=pool)

app = Celery('video', broker=CONFIG.CELERY['CELERY_BROKER_URL'], backend=CONFIG.CELERY['CELERY_RESULT_BACKEND'])

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    # celery beat schedule
    CELERYBEAT_SCHEDULE={
        'CAL_VIDEO_SCORE': {
            'task': 'cal_video_score',
            'schedule': crontab(minute='*/1'),
            'args': (),
        },
    }
)


def cal_video_score():
    videos = Video.select(Video.id).order_by(Video.id.desc())
    for video in videos:
        pipe = con.pipeline()  # redis pipeline
        likes = con.get(cs.REDIS_VIDEO_LIKE.format(video.id)) or 0
        watched = con.get(cs.REDIS_VIDEO_WATCH.format(video.id)) or 0
        comments = con.get(cs.REDIS_VIDEO_COMMENT.format(video.id)) or 0
        pipe.execute()

        score = int(likes) + int(watched) * 2 + int(comments) * 10  # cal video score

        con.zadd(cs.REDIS_VIDEO_RECOMMEND, {str(video.id): score})


@app.task
def add(x, y):
    pass


if __name__ == '__main__':
    cal_video_score()
