#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import argparse
from urllib.parse import urljoin

parser = argparse.ArgumentParser(description='i do')
parser.add_argument('city')
city = parser.parse_args().city


def make_url():
    city_dict = {
        '宜昌': 'yc',
        '武汉': 'wuhan',
        '重庆': 'cq',
        '北京': 'bj',
    }
    city_code = city_dict[city]
    base_url = 'http://zu.{}.fang.com'.format(city_code)
    # special
    if city_code == 'bj':
        base_url = 'http://zu.fang.com'

    url_list = list()

    for i in range(33, 100):
        url = base_url+'/house/i{}/'.format(i)
        url_list.append(url)

    return url_list


def get_houses(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    tags = soup.select('.houseList > dl')

    houses = list()
    for tag in tags:
        house = {
            'url': urljoin(url, tag.select('dt > a ')[0]['href']),
            'name': tag.select('dd > p > a')[0].string,
            'price': tag.select('.moreInfo > p > span')[0].string
        }
        houses.append(house)
    houses.sort(key=lambda x: x['price'])
    return houses
    # print(houses)


class MongoMagener(object):

    def __init__(self, url=None, port=None):
        self.url = url
        self.port = port

    def get_collection(self):
        client = MongoClient(host=self.url, port=self.port)
        db = client.jyy
        collection = db.jyy_zufang
        return collection

if __name__ == '__main__':
    # urls = make_url()
    # get_houses(urls[0])
    mongo = MongoMagener()
    collection_jyy = mongo.get_collection()
    for url in make_url():
        houses = get_houses(url)
        collection_jyy.insert(houses)
