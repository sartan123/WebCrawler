# -*- coding: utf-8 -*-
import os
import scrapy


class QiitaSpider(scrapy.Spider):
    name = 'anison'
    start_urls = ['http://www.jtw.zaq.ne.jp/animesong/ma/index.html']
    custom_settings = {
        "DOWNLuAD_DELAY": 3,
    }

    def parse(self, response):
        for key in [2, 3]:
            for href in response.xpath('/html/body/table/tr/td[{}]/a/@href'.format(key)):
                full_url = response.urljoin(href.extract())
                yield scrapy.Request(full_url, callback=self.parse2)

    def parse2(self, response):
        for href in response.xpath('//td/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        directry = str(response)
        directry = directry.split('/')
        if os.path.exists('./anison/{0}/{1}'.format(directry[4], directry[5])) is not True:
            print('{}ディレクトリ生成'.format(directry[5]))
            os.mkdir('./anison/{0}/{1}'.format(directry[4], directry[5]))
        kashi = response.xpath('//pre/text()').extract()
        kashi = kashi[0].split('\n')
        file = open('./anison/{0}/{1}/{2}.txt'.format(directry[4], directry[5], kashi[0]), 'w')
        for j in range(len(kashi)):
            file.write(kashi[j]+'\n')
        file.close()
