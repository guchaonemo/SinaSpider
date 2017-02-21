# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# -*- coding: utf-8 -*-

from scrapy import Item, Field


class InformationItem(Item):

    """The basic information"""
    uid = Field()
    NickName = Field()
    Gender = Field()
    Num_Tweets = Field()
    Num_Follows = Field()
    Num_Fans = Field()
    URL = Field()
