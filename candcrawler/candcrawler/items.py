# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags, replace_entities,replace_tags

def remove_whitespace(value):
    return value.strip()


class CandcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    search = scrapy.Field(
        input_processor = MapCompose(remove_tags,remove_whitespace),
        output_processor = TakeFirst()
        )

    link = scrapy.Field(
        input_processor = MapCompose(remove_whitespace),
        output_processor = TakeFirst()
        )

    headline = scrapy.Field(
        input_processor = MapCompose(remove_tags,remove_whitespace),
        output_processor = TakeFirst()
        )
    
    metadata = scrapy.Field(
        input_processor = MapCompose(remove_tags,remove_whitespace),
        output_processor = Join()
        )

    li_url = scrapy.Field(
        input_processor = MapCompose(remove_tags,remove_whitespace),
        output_processor = TakeFirst()
        )

    summary = scrapy.Field(
        input_processor = MapCompose(remove_tags,remove_whitespace,replace_entities,replace_tags),
        output_processor = Join()
        )
