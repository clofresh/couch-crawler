
from datetime import datetime

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from couchcrawler.items import IndexableItem

from couchcrawler.settings import config

class WikiSpider(CrawlSpider):
    ''' Can spider MediaWiki and Twiki wikis.
    '''
    
    domain_name = config.get('wiki', 'domain_name')
    extra_domain_names = config.get('wiki', 'extra_domain_names').split(',')
    start_urls = config.get('wiki', 'start_urls').split(',')
    
    rules = [
        Rule(SgmlLinkExtractor(deny=["\?", "Special:.*"]), 
             callback='parse_wiki', 
             follow=True),
    ]
    
    def parse_wiki(self, response):
        hxs = HtmlXPathSelector(response)
        
        item = IndexableItem()
        item['type'] = 'wiki'
        item['title'] = hxs.select('//title/text()').extract()[0]
        item['url'] = response.url
        item['mod_datetime'] = datetime.now().isoformat()

        to_exclude = ["[not(self::%s)]" % x for x in ["script", "style"]]
        content_xpath = "//body//*%s/text()" % ("".join(to_exclude))
        item['contents'] = "\n".join([
            s.strip() for s 
            in hxs.select(content_xpath).extract() 
            if s.strip()
        ])
        
        return item

SPIDER = WikiSpider()
