# -*- coding: utf-8 -*-
import re

import scrapy

from ebay.items import EbayItemShop, EbayItemGood

from scrapy_redis.spiders import RedisSpider


class EbaySpider(RedisSpider):
    name = 'ebay_goods'
    allowed_domains = ['ebay.com']
    redis_key = 'ebay:start_urls'

    # start_urls = 'https://www.ebay.com/n/all-categories'

    # def start_requests(self):
    #     yield scrapy.Request(url=self.start_urls,
    #                          callback=self.parse)

    custom_settings = {

    'SCHEDULER': "scrapy_redis.scheduler.Scheduler",

    'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    'REDIS_URL': 'redis://127.0.0.1:6379/1',

    'SCHEDULER_PERSIST': True,
    }



    # 一级分类
    def parse(self, response):
        category1_urls = response.xpath('//ul[@class="sub-cats"]/li/a/@href').getall()
        for category1_url in category1_urls:
            yield scrapy.Request(url=category1_url,
                                 callback=self.parse_category2)

    # 二级分类
    def parse_category2(self, response):
        category2_urls = []
        if response.xpath('//div[@class="srp-rail__left"]'):
            urls = response.xpath(
                '//div[@class="srp-rail__left"]//li[@class="srp-refine__category__item"]/a/@href').getall()
            for url in urls:
                category2_urls.append(url)
        elif response.xpath('//div[@class="dialog__cell"]'):
            urls = response.xpath('//div[@class="dialog__cell"]/section//li/a/@href').getall()
            for url in urls:
                category2_urls.append(url)
        for category2_url in category2_urls:
            yield scrapy.Request(url=category2_url,
                                 callback=self.parse_good)

    # 二级分类下列表页的商品url
    def parse_good(self, response):
        good_urls = []
        if response.xpath('//div[starts-with(@class,"srp-river-results")]'):
            urls = response.xpath('//ul[starts-with(@class,"srp-results")]//a[@class="s-item__link"]/@href').getall()
            for url in urls:
                good_urls.append(url)
        elif response.xpath('//section[starts-with(@class,"b-module b-list b-listing")]'):
            urls = response.xpath('//ul[@class="b-list__items_nofooter"]//a[@class="s-item__link"]/@href').getall()
            for url in urls:
                good_urls.append(url)
        for good_url in good_urls:
            yield scrapy.Request(url=good_url,
                                 callback=self.parse_seller)
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse_good)

    # 获取商家名称
    def parse_seller(self, response):

        seller_name = response.xpath(
            '//span[@class="mbg-nw"]/text()|//span[@class="app-sellerpresence__sellername"]/span/text()|//div[@class="seller-persona "]/span[2]/a[1]/text()').get()

        list_url = 'https://www.ebay.com/sch/%s/m.html?_nkw&_armrs=1&_from&rt=nc&LH_PrefLoc=6'
        if seller_name:


            list_url = list_url % seller_name

            yield scrapy.Request(url=list_url,
                                 callback=self.parse_list)

    # 获取商品url，和下一页url
    def parse_list(self, response):

        if response.xpath('//ul[@id="ListViewInner"]'):
            goods_urls = response.xpath('//ul[@id="ListViewInner"]/li/h3/a/@href').getall()

            for url in goods_urls:
                yield scrapy.Request(url=url,
                                    callback=self.parse_goodinfo)

                next_page = response.xpath('//td[@class="pagn-next"]/a/@href').get()
                if next_page:
                    yield scrapy.Request(url=next_page,
                                            callback=self.parse_list)

    # 获取商品详情
    def parse_goodinfo(self, response):

        good_id = re.search(r'itm.+/(\d+)', response.url).group(1)

        # 保存商品源码
        with open(r'D:/Spider_Demo/ebay/goods_html/' + good_id + '.html', 'a', encoding='utf-8') as f:
            f.write(response.text)

        good_name = response.xpath('//h1[@id="itemTitle"]/text()').get()
        price_dollar = response.xpath('//span[@id="prcIsum"]/@content').get()
        price_RMB = response.xpath('//div[@id="prcIsumConv"]/span/text()').get()
        if price_RMB != None:
            price_RMB = price_RMB.split()[1]
        project_location = response.xpath('//span[@itemprop="availableAtOrFrom"]/text()').get()
        brand = response.xpath('//span[@itemprop="name"]/text()').getall()
        if brand != []:
            brand = brand[-1]
        else:
            brand = ''
        seller_name = response.xpath(
            '//span[@class="mbg-nw"]/font/font/text()|//span[@class="mbg-nw"]/text()').get()
        sales_count = response.xpath('//a[@class="vi-txt-underline"]/text()').get()
        if sales_count != None:
            sales_count = sales_count.split()[0]
        else:
            sales_count = ''
        cats = response.xpath('//li[@class="bc-w"]//span/text()').getall()
        if len(cats) == 0:
            cat_1 = cat_2 = cat_3 = cat_4 = cat_5 = cat_6 = ''
        elif len(cats) == 1:
            cat_1 = cats[0]
            cat_2 = cat_3 = cat_4 = cat_5 = cat_6 = ''
        elif len(cats) == 2:
            cat_1, cat_2 = cats[0], cats[1]
            cat_3 = cat_4 = cat_5 = cat_6 = ''
        elif len(cats) == 3:
            cat_1, cat_2, cat_3 = cats[0], cats[1], cats[2]
            cat_4 = cat_5 = cat_6 = ''
        elif len(cats) == 4:
            cat_1, cat_2, cat_3, cat_4 = cats[0], cats[1], cats[2], cats[3]
            cat_5 = cat_6 = ''
        elif len(cats) == 5:
            cat_1, cat_2, cat_3, cat_4, cat_5 = cats[0], cats[1], cats[2], cats[3], cats[4]
            cat_6 = ''
        else:
            cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, = cats[0], cats[1], cats[2], cats[3], cats[4], cats[5]

        # 字段保存
        item = EbayItemGood(good_id=good_id, good_name=good_name, price_dollar=price_dollar, price_RMB=price_RMB,
                            project_location=project_location, brand=brand, seller_name=seller_name,
                            sales_count=sales_count, cat_1=cat_1, cat_2=cat_2, cat_3=cat_3, cat_4=cat_4,
                            cat_5=cat_5,
                            cat_6=cat_6)
        yield item
