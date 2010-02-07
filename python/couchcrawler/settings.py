# Scrapy settings for couchcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'couchcrawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['couchcrawler.spiders']
NEWSPIDER_MODULE = 'couchcrawler.spiders'
DEFAULT_ITEM_CLASS = 'couchcrawler.items.CouchCrawlerItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [
    'couchcrawler.pipelines.CouchCrawlerPipeline'
]

from ConfigParser import ConfigParser
config = ConfigParser()
config.read(['couchcrawler.cfg'])

