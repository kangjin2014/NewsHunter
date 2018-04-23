# the spider is use to automatically pull links from defined paths
import scrapy
import sys
import yaml

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html',
    ]
    
    def parse(self, response):															
        filename = 'new.html'
        with open(filename, 'wb') as f:
            f.write(response.body) 