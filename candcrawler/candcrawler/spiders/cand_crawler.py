# -*- coding: utf-8 -*-

import scrapy
from candcrawler.items import CandcrawlerItem
from scrapy.loader import ItemLoader
import urllib
import csv

class CandSpider(scrapy.Spider):
    name = 'bingcrawler'
    start_urls = []
    export = []
    custom_settings = {
            'FEED_URI': 'bing_cralwer.csv',
            'FEED_FORMAT': 'csv',
            'FEED_EXPORT_ENCODING': 'utf-8-sig',
            'FEED_EXPORT_FIELDS': [
                'headline',
                'summary',
                'metadata',
                'li_url',
                'search',
                'link',
                'cand_name',
                'cand_detail'
             ],
         }
    with open('input\\cand_list_title.csv', 'r') as csvfile:
        next(csvfile)
        filereader = csv.reader(csvfile)
        for row in filereader:
            data = ("http://www.bing.com/search?q=%s" % (urllib.parse.quote_plus(row[0] + ' ' + row[1])),
                              row[0],
                              row[1])
            start_urls.append(data)

    def start_requests(self):
        for item in self.start_urls:
            yield scrapy.Request(url=item[0], 
                                 callback=self.parse, 
                                 errback=self.errback
                                 )         # actual web crawling
            
    def parse(self, response):
        for i in range(1,11): #range to 10 because bing results are 10 per page
            for row in response.xpath("//li[@class='b_algo'][%s]" % i):
                l = ItemLoader(item=CandcrawlerItem(), selector = row)
                l.add_xpath("headline",  "h2//text()")
                l.add_xpath("metadata", "div[@class='b_caption']/div[@class='b_factrow b_twofr']/div[@class='b_vlist2col']/ul/li/div//text()")
                l.add_xpath("li_url", "div[@class='b_caption']/div[@class='b_attribution']/cite/text()")
                l.add_xpath("summary", "div[@class='b_caption']/p//text()")
                l.add_xpath("search", "//div[@class='b_searchboxForm']/input/@value")
                l.add_value("link", response.request.url)
				#this is to get only the LinkedIn results
                if 'linkedin.com/in' in response.xpath("//li[@class='b_algo'][%s]/div[@class='b_caption']/div[@class='b_attribution']/cite/text()" % i).get():
                    yield l.load_item()
                else:
                   pass
                    
        next_page = response.xpath("//li[@class='b_pag']/nav/ul/li/a[@aria-label='Page 2']/@href").get()
        if next_page is not None:
            next_page = "http://www.bing.com" + next_page
            yield response.follow(next_page, callback = self.parse)
            
    def errback(self, failure):
        self.logger.info('Handled by the errback: %s (%s exception)', failure.request.url, str(failure.value))
        yield {"summary": 'ERROR',
                "link": str(failure.request.url)
                }
