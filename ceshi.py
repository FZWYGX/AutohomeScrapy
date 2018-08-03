import requests
from scrapy import Selector
import re
import os


class BmwPipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '汽车之家')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def run(self):
        url = 'https://car.autohome.com.cn/pic/series/202-10.html'

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        resp = requests.get(url, headers=headers)

        response = Selector(text=resp.text)

        path_list = response.xpath("//div[@class='breadnav']//text()").extract()
        path_list = [i.strip() for i in path_list if len(i.strip()) > 0
                     and ("当前位置" not in i) and (">" not in i)
                     and ("汽车之家" not in i) and ("汽车图片" not in i)]
        path_list = "/".join(path_list)
        print(self.path)
        print(path_list)

        path_detail = os.path.join(self.path, path_list)
        if not os.path.exists(path_detail):
            os.makedirs(path_detail)
        print(path_detail)


if __name__ == '__main__':
    bmw = BmwPipeline()
    bmw.run()

