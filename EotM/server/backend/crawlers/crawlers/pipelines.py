# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.append('/Users/vaheh/Downloads/Thesis/myinalyze/EotM/server/backend/')
print(sys.path)
from dbInterface import DBInterface
#from scrapy import log
from scrapy.exceptions import DropItem


class uberTrendsMongoDB:



    def process_item(self, item, spider):

        collection_name = 'ubertrends'

        DBInterface.initialize('eotm')
        print(DBInterface.get_colletions())

        DBInterface.insert_one('ubertrends', item)
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        # if valid:
        #     self.collection.insert(dict(item))
        #     log.msg("trends added to MongoDB database!",
        #             level=log.DEBUG, spider=spider)
        return item
