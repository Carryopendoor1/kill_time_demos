#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-11-6 下午3:32
# @Author  : Jyy
# @Site    : 
# @File    : run_app.py
# @Software: PyCharm
from __future__ import division, print_function
from gevent.pywsgi import WSGIServer
from application import get_application

if __name__ == "__main__":
    app = get_application()
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
