# -*- coding: utf-8 -*-
import scrapy
from ..items import A51JobItem
from scrapy.linkextractors import LinkExtractor
from copy import deepcopy
class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']

    def parse(self, response):
        # print(response.text)
        item = A51JobItem()
        for each in response.xpath('//div[@class="el"]'):
            item["name"] = each.xpath('./p/span/a/@title').extract_first()
            add = each.xpath('./span[@class="t3"]/text()').extract()
            item["add"] = add[0] if add else None
            money = each.xpath('./span[@class="t4"]/text()').extract()
            item["money"] = money[0] if money else None
            item['date'] = each.xpath('./span[@class="t5"]/text()').extract_first()
            # item = deepcopy(item)
            yield item
        le = LinkExtractor(restrict_xpaths='//div[@class="p_in"]/ul/li')
        le_list = le.extract_links(response)
        if le_list:
            for each in le_list:
                url = each.url
                yield scrapy.Request(url,callback=self.parse)
