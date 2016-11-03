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

city_dict = {
    '宜昌': 'yc',
    '武汉': 'wuhan',
    '重庆': 'cq',
    '北京': 'bj',
}
base_url = ''


class Spiderv1Spider(scrapy.Spider):
    name = 'spider_v_1'

    def start_requests(self):
        global base_url
        city = getattr(self, 'city', None)
        city_code = city_dict[city]

        base_url = 'http://zu.{}.fang.com'.format(city_code)

        static_urls = []
        for i in range(33, 34):
            url = base_url + '/house/i{}/'.format(i)
            static_urls.append(url)
        for url in static_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global base_url
        # items = []
        for house in response.css('div.houseList dl'):
            item = ScrapZufangItem()
            item['name'] = ''.join(house.css('dd p a::attr(title)').extract())
            item['url'] = ''.join(house.css('dt a::attr(href)').extract())
            item['price'] = ''.join(house.css('dd div.moreInfo p span::text').extract())
            # items.append(item)
            yield item
        # return items

