#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-11-6 下午3:29
# @Author  : Jyy
# @Site    : 
# @File    : model.py
# @Software: PyCharm
from __future__ import division, print_function
from gevent import queue


class Room(object):
    def __init__(self):
        self.users = set()
        self.messages = []

    def backlog(self, size=25):
        return self.messages[-size:]

    def subscribe(self, user):
        self.users.add(user)

    def add(self, message):
        for user in self.users:
            print(user)
            user.queue.put_nowait(message)
        self.messages.append(message)


class User(object):
    def __init__(self):
        self.queue = queue.Queue()
