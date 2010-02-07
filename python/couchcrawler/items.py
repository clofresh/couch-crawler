# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CouchCrawlerItem(Item):
    url = Field()
    contents = Field()
    title = Field()
    mod_datetime = Field()
