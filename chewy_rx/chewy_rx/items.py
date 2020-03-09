# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChewyRxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product = scrapy.Field()
    brand = scrapy.Field()
    discount = scrapy.Field()
    regular = scrapy.Field()
    categories = scrapy.Field()
    num_review = scrapy.Field()
    star = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    #rating = scrapy.Field()

