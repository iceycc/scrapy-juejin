# -*- coding: utf-8 -*-
import scrapy
import json


# from bs4 import BeautifulSoup


class HomeSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'home'
    allowed_domains = ['juejin.im']
    # 起始URL列表
    start_urls = [
        'https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed']

    def start_requests(self):
        form_data = {"id_type": '2', "client_type": '2608',
                     "sort_type": '300', "cursor": "0", "limit": '20'}
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=form_data)

    def getTitle(self):
        pass

    def parse(self, response):
        filename = response.url.split("/")[-2]
        body = response.body
        data = json.loads(body)['data']
        with open('list2.json', 'wb') as f:
            f.write(json.dumps(data))
        for i in range(len(data)):
            item_info = data[i].get('item_info')
            try:
                print(item_info.get('article_info').get('title'))
            except AttributeError as e:
                pass

    # def parse2(self, response):
    #     filename = response.url.split("/")[-2]
    #     body = response.body
    #     data = json.loads(body)['data']
    #     with open('list2.json', 'w') as f:
    #         f.write(json.dumps(data))
    #     for i in range(len(data)):
    #         item_info = data[i].get('item_info')
    #         print(item_info)
    #         # print(item_info.get('article_info'))
