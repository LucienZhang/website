# -*- coding: utf-8 -*-
# @Author: Lucien Zhang
# @Date:   2019-09-19 17:55:24
# @Last Modified by:   Lucien Zhang
# @Last Modified time: 2019-09-22 19:07:18
from .ml_module import ml_api


def init_app(app, prefix):
    app.register_blueprint(ml_api, url_prefix=prefix)