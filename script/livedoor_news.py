# -*- coding: utf-8 -*-
import scrapy
import re


class NewsSpider(scrapy.Spider):
    name = 'livedoor_news'

    # エンドポイント（クローリングを開始するURLを記載する）
    start_urls = ['http://news.livedoor.com/']

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    # URLの抽出処理を記載
    def parse(self, response):
        for href in response.xpath("//div/ul[@class='topicsList']/li/a/@href"):
            full_url = response.urljoin(href.extract())
            full_url = full_url.replace('topics', 'article')
            yield scrapy.Request(full_url, callback=self.parse_item)

    # ダウンロードしたページを元に、内容を抽出し保存するItemを作成
    def parse_item(self, response):
        file = open('livedoor_news.txt', 'a')
        text = response.xpath("//div[@class='articleBody']/span[@itemprop='articleBody']/text()")
        news = text.extract()
        for line in news:
            line = re.sub(r'(<.*?>)|(\n)|(\s*)', '', line, re.MULTILINE)
            file.write(line)
