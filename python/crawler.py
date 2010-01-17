import sys
from datetime import datetime
from urlparse import urlparse

import httplib2
from couchdb.client import Server, ResourceNotFound
from BeautifulSoup import BeautifulSoup

class UrlException(Exception):
    def __init__(self, message, url, response={}):
        message = '%s: %s (%s)' % (message, url, repr(response))
        Exception.__init__(self, message)

class UrlNotFound(UrlException):
    def __init__(self, url, response):
        UrlException.__init__(self, "Url not found", url, response)

class HostNotFound(UrlException):
    def __init__(self, url):
        UrlException.__init__(self, "Host not found", url)

class NotHtml(UrlException):
    def __init__(self, url, response):
        UrlException.__init__(self, "Not an html document", url, response)


class HtmlDoc(object):
    def __init__(self, url, soup, mod_datetime=None):
        self.url = url
        self.soup = soup
        self.mod_datetime = mod_datetime or datetime.now()
    
    @classmethod
    def from_url(cls, url):
        http_client = httplib2.Http()
        
        try:
            response, body = http_client.request(url)

            if response['status'] != '200':
                raise UrlNotFound(url, response)
            elif response['content-type'].find('text/html') == -1:
                raise NotHtml(url, response)
            else:
                return cls(url, BeautifulSoup(body))
        except httplib2.ServerNotFoundError, e:
            raise HostNotFound(url)
        
    
    @property
    def title(self):
        return self.soup.title.string            
    
    @property
    def contents(self):
        for element in self.soup.recursiveChildGenerator():
            if isinstance(element, unicode):
                yield element
    
    @property
    def outbound_urls(self):
        for element in self.soup.findAll('a'):
            if element.get('href', None) is None:
                continue
                
            href = element['href']
            
            if href[0] == '#':
                continue
            
            if href[0] == '/':
                url_parts = urlparse(self.url)
                href = "%s://%s%s" % (
                    url_parts.scheme,
                    url_parts.netloc, 
                    href
                )
            
            if urlparse(href).scheme not in ['http', 'https']:
                continue
            
            yield href

    
    def to_dict(self):
        return {
            "url":          self.url,
            "contents":     ''.join(self.contents),
            "title":        self.title,
            "mod_datetime": self.mod_datetime.isoformat(),
        }

def index(url, max_depth, couchdb_conn, seen_already=set()):
    if url not in seen_already:
        seen_already.add(url)
    
        print url

        try:
            html_doc = HtmlDoc.from_url(url)
            load(html_doc, couchdb_conn)
    
            if max_depth > 0:
                for u in html_doc.outbound_urls:
                    newly_seen = index(u, max_depth - 1, couchdb_conn, seen_already)
                    seen_already.union(newly_seen)
        except UrlException, e:
            print >> sys.stderr, str(e)
    
    return seen_already

def load(html_doc, couchdb_conn):
    try:
        del couchdb_conn[html_doc.url]
    except ResourceNotFound:
        pass
    
    couchdb_conn[html_doc.url] = html_doc.to_dict()


def usage():
    return '''Usage: python crawler.py [-d max_depth] [-c couchdb_url] url1 [url2 [url3 [...]]]'''
    
if __name__ == '__main__':
    from optparse import OptionParser
    
    parser = OptionParser()
    
    defaults = {
        'max_depth': 3,
        'couchdb_url': 'http://localhost:5984/crawler'
    }
    
    parser.add_option(
        '-d', '--max-depth', 
        action="store", dest='max_depth', 
        type="int", default=defaults['max_depth'],
        help="Don't follow links past this depth. Default: %d" % defaults['max_depth']
    )
    parser.add_option('-c', '--couchdb-url', 
        action="store", dest='couchdb_url',
        type="string", default=defaults['couchdb_url'],
        help="Url to couchdb database. Default: %s" % defaults['couchdb_url']
    )

    options, args = parser.parse_args()
    max_depth = options.max_depth
    couch_url_parts = urlparse(options.couchdb_url)

    if couch_url_parts.scheme == '':
        host = "http://%s" % couch_url_parts.netloc
    else:
        host = "%s://%s" % (couch_url_parts.scheme, couch_url_parts.netloc)

    db_name = couch_url_parts.path.split('/')[1]
    couchdb_conn = Server(host)[db_name]
    
    if len(args) == 0:
        print >> sys.stderr, usage()
        sys.exit(1)
    
    for url in args:
        if urlparse(url).scheme == '':
            url = 'http://' + url
            
        index(url, options.max_depth, couchdb_conn)
        


