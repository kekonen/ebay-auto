# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tinydb import TinyDB, Query
from scrapy import log
from scrapy.exceptions import IgnoreRequest


class EbayAutoPipeline(object):
    def process_item(self, item, spider):
        return item


class SkipURL(object):
    def __init__(self):
        self.db = TinyDB('./urls.json')

    def process_item(self, item, spider):
        url = item['url']
        self.db.insert({'url': url})
        spider.added += 1
        return item
