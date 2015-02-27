# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.exceptions import DropItem

from engrscrape.dbhandler import has_url, add_url, add_outlinks

# Filters any duplicate links from the incoming stream
class FilterDuplicatesPipeline(object):
    """ A pipeline for filtering out duplicate links in the url table """

    def __init__(self):
        self.conn = sqlite3.connect('./links.sqlite')

    def process_item(self, item, spider):
        if has_url(self.conn, item):
            raise DropItem("Already added '{}'".format(item['url']))
        return item

# Actually adds the data to the database
class AddItemToDatabasePipeline(object):
    """ A pipeline for adding filtered results to the database """

    def __init__(self):
        self.conn = sqlite3.connect('./links.sqlite')

    def process_item(self, item, spider):
        add_url(self.conn, item)
        add_outlinks(self.conn, item)

