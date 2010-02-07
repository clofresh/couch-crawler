# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from couchdb.client import Server, ResourceNotFound
from couchcrawler.settings import config

class CouchCrawlerPipeline(object):
    def __init__(self):
        server = Server(config.get('couchdb', 'host'))
        self.conn = server[config.get('couchdb', 'db')]
    
    def process_item(self, domain, item):
        url = item['url']
        
        try:
            doc = self.conn[url]
            for key, val in item.iteritems():
                doc[key] = val
        except ResourceNotFound:
            self.conn[url] = dict(item)
        
        return item
