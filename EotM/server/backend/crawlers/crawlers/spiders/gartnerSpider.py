# -*- coding: utf-8 -*-
import scrapy

class GartnerSpider(scrapy.Spider):
    # This is the spider for ubertrends, it gets the uber categories from forrester and gartner
    name = 'gartnerSpider'
    # Only requests to this website will be considered for crawling. If you wish to extend the list, add domains here.
    allowed_domains = ['www.gartner.com']
    # List of URLs to be scraped
    start_urls = ['https://www.gartner.com/smarterwithgartner/gartner-top-10-strategic-technology-trends-for-2020/']

    def parse(self, response):
        # Extracting the content using css selectors
        titles = response.xpath('/html/body/div[1]/div/main/section[2]/div/div[2]/article/div[2]/h2/text()').extract()

        # Give the extracted content row wise
        for title in titles:
            # create a dictionary to store the scraped info
            item = {}
            item['trend'] = title.split(' ')[-1]
            item['url'] = 'https://www.gartner.com/smarterwithgartner/gartner-top-10-strategic-technology-trends-for-2020/'
            item['source'] = 'Gartner'
            item['ranking'] = 0

            # yield or give the scraped info to scrapy
            yield item