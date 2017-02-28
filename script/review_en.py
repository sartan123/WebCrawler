# -*- coding: utf-8 -*-
import re
import time
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup


# レビューと評価をスクレイピング
def scraping(url):
    url = requests.get(url)
    text = url.text
    result = BeautifulSoup(text, "lxml")
    review_rates = result.find_all("div", class_="rating reviewItemInline")
    review_text = result.find_all("p", id=re.compile(r'review_[0-9].*?'))
    for review_rate, review_text in zip(review_rates, review_text):
        rating = str(review_rate)
        rate = re.search(r'([0-5])\sof\s5', rating)
        text = review_text.text.lstrip('\n')
        print(title + '\t' + rate.group(1) + '\t' + text, file=output)


# 次のページに移動
def crawling(url):
    url = requests.get(url)
    text = url.text
    result = BeautifulSoup(text, "lxml")
    next_url = result.find(
        "a", class_="nav next rndBtn ui_button primary taLnk")
    next_url = urljoin(original_url, next_url['href'])
    return next_url


# 観光地のメインページからレビューページに飛ぶ
def search_url(url):
    url = requests.get(url)
    text = url.text
    result = BeautifulSoup(text, "lxml")
    next_url = result.find_all("a")
    for url in next_url:
        if 'html#REVIEWS' in str(url):
            next_url = urljoin(original_url, url['href'])
            return next_url
    return None   # レビューがなければ(そんなことないと思うけど)

if __name__ == '__main__':
    output = open('review_en.txt', 'a')
    url_list = open('url_list.txt')
    url_list = url_list.readlines()
    for url in url_list:
        url = url.rstrip('\n')
        url = url.split(' ')
        title = url[0]
        print(title)
        original_url = url[1]
        original_url = search_url(original_url)
        scraping(original_url)
        next_url = crawling(original_url)
        while next_url:   # 再帰的にページを移動
            time.sleep(1)   # アクセス拒否対策
            scraping(next_url)
            try:   # 次のページがなければ終了
                next_url = crawling(next_url)
            except:
                break
