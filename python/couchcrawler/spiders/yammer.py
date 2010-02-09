import json

from oauth.oauth import OAuthConsumer, OAuthSignatureMethod_PLAINTEXT, OAuthRequest, OAuthToken

from scrapy.spider import BaseSpider
from scrapy.http import Request

from couchcrawler.items import YammerItem
from couchcrawler.settings import config

class YammerSpider(BaseSpider):
    domain_name = 'yammer.com'
    start_urls = [config.get('yammer', 'json_messages_url')]

    def __init__(self, domain_name=None):
        BaseSpider.__init__(self, domain_name)

        consumer_key    = config.get('yammer', 'consumer_key')
        consumer_secret = config.get('yammer', 'consumer_secret')
        app_token       = config.get('yammer', 'app_token')

        self.consumer  = OAuthConsumer(consumer_key, consumer_secret)
        self.signature = OAuthSignatureMethod_PLAINTEXT()
        self.token     = OAuthToken.from_string(app_token)
    
    def make_requests_from_url(self, url):
        oauth_request = OAuthRequest.from_consumer_and_token(
                                            self.consumer,
                                            token=self.token,
                                            http_method='GET',
                                            http_url=url)
        oauth_request.sign_request(self.signature, self.consumer, self.token)

        return Request(oauth_request.to_url(), callback=self.parse, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body)
        
        for message in data['messages']:
            item = YammerItem()
            item['type'] = 'yammer'
            item['url'] = message['web_url']

            body = message['body']['plain']
            item['contents'] = body
            
            max_title_length = 40
            if len(body) > 40:
                item['title'] = body[0:max_title_length - 3] + '...'
            else:
                item['title'] = body

            item['mod_datetime'] = message['created_at']
            item['author'] = message['sender_id']
            item['parent_url'] = message['replied_to_id']
            item['thread_url'] = message['thread_id']
            item['likes'] = message['liked_by']
            
            yield item

SPIDER = YammerSpider()
