# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class DcontentsItem(Item):
    id = Field()
    title = Field()
    year = Field()
    score = Field()
    director = Field()
    classification = Field()
    actor = Field()
    feature = Field()
