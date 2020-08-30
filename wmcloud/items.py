# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WmcloudItem(scrapy.Item):
    # define the fields for your item here like:
    symbol = scrapy.Field()
    total = scrapy.Field()
    percent = scrapy.Field()
    quality = scrapy.Field()
    industry = scrapy.Field()
    institution = scrapy.Field()
    valuation = scrapy.Field()
    trend = scrapy.Field()
    quality_content = scrapy.Field()
    quality_tag = scrapy.Field()
    strategy_content = scrapy.Field()
    strategy_tag = scrapy.Field()
    risk = scrapy.Field()
    pass
