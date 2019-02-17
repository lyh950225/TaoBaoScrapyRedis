# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


class TaobaoscrapyredisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    buy = scrapy.Field()
    shop = scrapy.Field()
    shop_url = scrapy.Field()
    location = scrapy.Field()
    dsec = scrapy.Field()


class TaobaoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

