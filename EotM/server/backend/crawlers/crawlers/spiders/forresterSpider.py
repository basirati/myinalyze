# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from crawlers.items import ForresterItem


class ForresterSpider(scrapy.Spider):
    # This is the spider for ubertrends, it gets the uber categories from forrester and gartner
    name = 'forresterSpider'
    # Only requests to this website will be considered for crawling. If you wish to extend the list, add domains here.
    allowed_domains = ['go.forrester.com']
    # List of URLs to be scraped
    start_urls = ['https://go.forrester.com/research/predictions/']


    def parse(self, response):
        # Extracting the content using css selectors
        titles = response.xpath('//*[@id="main"]/section[2]/div/div/div/div[2]/div/h3/text()').extract()

        #trends = {}
        # Give the extracted content row wise
        for title in titles:
            # create a dictionary to store the scraped info
            item = {}
            item['trend'] = title
            item['url'] = 'https://go.forrester.com/research/predictions/'
            item['source'] = 'Forrester'
            item['ranking'] = 0

            # yield or give the scraped info to scrapy
            yield item



