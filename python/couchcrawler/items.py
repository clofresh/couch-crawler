# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class IndexableItem(Item):
    url = Field()
    contents = Field()
    title = Field()
    mod_datetime = Field()
    type = Field()

class YammerItem(IndexableItem):
    url = Field()
    contents = Field()
    title = Field()
    mod_datetime = Field()
    type = Field()

    author = Field()
    parent_url = Field()
    thread_url = Field()
    likes = Field()
