#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-11-6 下午3:35
# @Author  : Jyy
# @Site    : 
# @File    : application.py
# @Software: PyCharm
from __future__ import division, print_function
from flask import Flask
from chat_room.view import app as blue
import os

def get_project_dir():
    return os.path.split(os.path.abspath(__file__))[0]

def get_application():
    proj_dir = get_project_dir()
    flask_params = {
        'static_folder': os.path.join(proj_dir, 'static'),
        'template_folder': os.path.join(proj_dir, 'template'),
    }

    app = Flask('chat_room', **flask_params)
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # blueprints

    app.register_blueprint(blue)
    return app