# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import AutohomeItem
from scrapy_redis.spiders import RedisCrawlSpider


class CarpicSpider(RedisCrawlSpider):
    name = 'carpic'
    allowed_domains = ['car.autohome.com.cn']
    # 汽车之家的导航栏
    # start_urls = ['https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0']
    redis_key = 'carpic:start_urls'

    rules = (
        # 匹配车的分类信息, 匹配翻页
        Rule(LinkExtractor(allow=r'/pic/series/\d+\-\d+\.html.*'), callback='parse_detail', follow=True),
        # 匹配车的类型
        Rule(LinkExtractor(allow=r'/pic/series/\d+\.html'), follow=True),
        # 匹配车的列表页
        Rule(LinkExtractor(allow=r'/pic/brand-\d+.html')),
        # 对于停产的车, 在series后面有-t
        # Rule(LinkExtractor(allow=r'/pic/series-t/\d+\-.+'), callback='parse_detail', follow=True),
        # 对于停产的车, 在series后面有-t
        # Rule(LinkExtractor(allow=r'/pic/series-t/\d+\.html'), follow=True),
    )

    def parse_detail(self, response):
        print(response.url)
        # 定位车的类型, 例如：（当前位置： 汽车之家 > 汽车图片 >  凯迪拉克 >  上汽通用凯迪拉克 >  凯迪拉克ATS-L）
        path_list = response.xpath("//div[@class='breadnav']//text()").extract()
        # 过滤掉"当前位置：", ">", "汽车之家", "汽车图片"
        path_list = [i.strip() for i in path_list if len(i.strip()) > 0
                     and ("当前位置" not in i) and (">" not in i)
                     and ("汽车之家" not in i) and ("汽车图片" not in i)]
        path_list = "/".join(path_list)
        # path_list即是文件的路径
        print(path_list)
        # 解析分类: 例如：　车身外观, 中控方向盘, 车厢座椅, 其它细节, 评测, 重要特点
        category = response.xpath("//div[@class='uibox']/div/text()").extract_first()
        # 解析每一个分类下的图片链接
        srcs = response.xpath("//div[contains(@class, 'uibox-con')]/ul/li//img/@src").extract()

        # 替换大图链接
        srcs = list(map(lambda x: x.replace("t_", ""), srcs))
        # 提取的链接不完整, 进行urljoin拼接
        urls = []
        for src in srcs:
            url = response.urljoin(src)
            urls.append(url)
        srcs = urls

        item = AutohomeItem(category=category, image_urls=srcs, path_list=path_list, url=response.url)
        print(item)
        yield item
