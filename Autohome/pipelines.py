# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import AutohomeItem
import os
from Autohome import settings
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from traceback import format_exc
from .items import *


class AutohomePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用
        # 其实这个方法本身就是去发送下载请求的
        request_objs = super(AutohomePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super(AutohomePipeline, self).file_path(request, response, info)
        path_list = request.item.get('path_list')
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        pic_path = os.path.join(images_store, path_list + "/" + category)
        print(pic_path)
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        image_name = path.replace("full/", "")
        image_path = os.path.join(pic_path, image_name)
        return image_path


class AutohomeMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['Carpic'] .ensure_index('url', unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, AutohomeItem):
                self.db['car'].update({'url': item['url']}, {'$set': item}, upsert=True)
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')
        except Exception as e:
            spider.logger.error(format_exc())
        return item