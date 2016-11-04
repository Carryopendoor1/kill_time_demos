# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrap_zufang import settings
from scrapy.exceptions import DropItem
from scrapy import log
from redis import StrictRedis


class ScrapZufangPipeline(object):
    def __init__(self):
        host = settings.MONGODB_SERVER
        port = settings.MONGODB_PORT
        db = settings.MONGODB_DB
        coll = settings.MONGODB_COLLECTION

        client = MongoClient(host=host, port=port)
        db = getattr(client, db, 'test')
        coll = getattr(db, coll)
        self.collection = coll

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.update_one({'name': item['name']}, {'$set': dict(item)}, upsert=True)
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

class ScrapZufangPipeLine_Redis(object):

    def __init__(self):
        host = settings.REDIS_SERVER
        port = settings.REDIS_PORT
        db = settings.REDIS_DB

        self.r = StrictRedis(host, port, db)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('miss {}'.format(data))
        if valid:
            pipe = self.r.pipeline()
            pipe.zadd('test', item['price'], str(item['name']).encode('utf-8'))
            pipe.execute()

