# -*- coding: utf-8 -*-
# @Author  : itswcg
# @File    : app.py
# @Time    : 18-12-20 上午11:14
# @Blog    : https://blog.itswcg.com
# @github  : https://github.com/itswcg

from sanic import Sanic
from sanic_cors import CORS
from app.config import CONFIG
from app.db import init_db, close_db
from app.api.views import api_bp

app = Sanic('video')
app.config.from_object(CONFIG)
CORS(app, automatic_options=True)  # cors

app.register_listener(init_db, 'before_server_start')
app.register_listener(close_db, 'after_server_stop')

app.blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=app.config['DEBUG'], access_log=app.config['ACCESS_LOG'])
