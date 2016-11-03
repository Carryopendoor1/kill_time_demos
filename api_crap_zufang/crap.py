#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

import argparse

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
    print(url_list)

if __name__ == '__main__':
    make_url()
