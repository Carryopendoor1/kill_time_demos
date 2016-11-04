#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-11-3 下午3:48
# @Author  : Jyy
# @Site    : 
# @File    : spider_v_1.py
# @Software: PyCharm
from __future__ import division, print_function
import scrapy
from urllib.parse import urljoin
from scrap_zufang.items import ScrapZufangItem
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

city_dict = {
    '宜昌': 'yc',
    '武汉': 'wuhan',
    '重庆': 'cq',
    '北京': 'bj',
}


class Spiderv1Spider(scrapy.Spider):
    name = 'spider_v_1'

    def start_requests(self):
        city = getattr(self, 'city', None)
        city_code = city_dict[city]
        if city == 'bj':
            base_url = 'http://zu.fang.com'
        else:
            base_url = 'http://zu.{}.fang.com'.format(city_code)

        static_urls = []
        for i in range(33, 34):
            url = base_url + '/house/i{}/'.format(i)
            static_urls.append(url)
        for url in static_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        for house in response.css('div.houseList dl'):
            item = ScrapZufangItem()
            url = ''.join(house.css('dt a::attr(href)').extract())
            item['name'] = ''.join(house.css('dd p a::attr(title)').extract())
            item['url'] = urljoin(str(response.url), url)
            item['price'] = ''.join(house.css('dd div.moreInfo p span::text').extract())
            items.append(item)
        items.sort(key=lambda x: x['price'])
        return items
        # return items


class Spiderv2Spider(CrawlSpider):
    name = 'spider_v_2'

    allowed_domains = ['fang.com']

    start_urls = [
        'http://zu.fang.com/house'
    ]

    rules = (

        Rule(LinkExtractor(allow='http://zu.(\w*).?fang.com/$'), callback='parse_zufang', follow=True),
    )

    def parse_zufang(self, response):
        for i in range(3, 7):
            url = str(response.url) + 'house/i3{}'.format(i)
            # urls.append(url)
            yield scrapy.Request(url, callback=self.parse_zufang_2)

    def parse_zufang_2(self, response):
        print(response.url)
        items = []
        for house in response.css('div.houseList dl'):
            item = ScrapZufangItem()
            url = house.css('dt a::attr(href)').extract_first()
            item['name'] = house.css('dd p a::attr(title)').extract_first()
            item['url'] = urljoin(str(response.url), url)
            item['price'] = house.css('dd div.moreInfo p span::text').extract_first()
            item['city'] = str(response.url).split('.')[1]
            items.append(item)
        items.sort(key=lambda x: x['price'])
        return items