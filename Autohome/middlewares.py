# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .Utils_Model.UserAgent import USER_AGENT
import logging
import requests
from twisted.internet.defer import DeferredLock
import random
from datetime import datetime, timedelta


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.update_time = datetime.now()
        self.proxy_wrong = True
        self.lock = DeferredLock()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'))

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        print("进入了ip代理的process_request")
        self.lock.acquire()
        if request.meta.get('retry_times') or self.proxy_wrong or self.is_expiring:
            print("我要去修改ip代理")
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri
                print('使用代理:' + uri)
                self.proxy_wrong = False
                self.update_time = datetime.now()
        self.lock.release()

    def process_response(self, request, response, spider):
        if response.status != 200:
            self.proxy_wrong = True
            return request
        return response

    @property
    def is_expiring(self):
        now = datetime.now()
        if (now - self.update_time) > timedelta(seconds=30):
            self.update_time = datetime.now()
            print("执行了is_expiring")
            return True
        else:
            return False


class UAMiddleware(object):
    def __init__(self):
        self.lock = DeferredLock()
        self.update_time = datetime.now()
        self.UA_List = USER_AGENT

    def process_request(self, request, spider):
        self.lock.acquire()
        if self.is_expiring:
            ua = random.choices(self.UA_List)
            request.headers['User-Agent'] = ua
            print(request.headers['User-Agent'])
        self.lock.release()

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    @property
    def is_expiring(self):
        now = datetime.now()
        if (now - self.update_time) > timedelta(seconds=30):
            self.update_time = datetime.now()
            print("跟换USER_AGENT")
            return True
        else:
            return False