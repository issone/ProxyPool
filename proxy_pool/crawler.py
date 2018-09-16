#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if k.startswith('crawl_'):
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip ').items()
            for td in tds:
                td.find('[style="display: none;"]').remove()
                td.find('[style="display:none;"]').remove()
                yield td.text().replace('\n', '')

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip, port])

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            trs = doc('table tr:gt(0)').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_89ip(self):
        for i in range(1, 3):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('tbody tr').items()

                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            l2s = doc('.l2').items()

            for l2 in l2s:
                ip = l2.find('span:nth-child(1)').text()
                port = l2.find('.port').text()
                yield ':'.join([ip, port])


if __name__ == '__main__':
    pass
