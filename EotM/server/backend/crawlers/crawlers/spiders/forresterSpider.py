# -*- coding: utf-8 -*-
import scrapy


class ForresterSpider(scrapy.Spider):
    # This is the spider for ubertrends, it gets the uber categories from forrester and gartner
    name = 'forresterSpider'
    # Only requests to this website will be considered for crawling. If you wish to extend the list, add domains here.
    allowed_domains = ['go.forrester.com']
    # List of URLs to be scraped
    start_urls = ['https://go.forrester.com/research/predictions/']

    def parse(self, response):
        # Extracting the content using css selectors
        titles = response.css('h3::text').getall()

        # Give the extracted content row wise
        for item in titles:
            # create a dictionary to store the scraped info
            scraped_info = {
                'trend': item
            }


            # yield or give the scraped info to scrapy
            yield scraped_info


    # def parse_item(self, response):
    #
    #
    #     item = scrapy.Item()
    #
    #     item['title'] = response.xpath('//h3::text').getall()
    #     # for h3 in response.xpath('//h3').getall():
    #     #     yield {"title": h3}
    #     print(item)
    #     return item
