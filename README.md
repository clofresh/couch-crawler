Couch Crawler 
=============

A search engine built on top of couchdb-lucene.

Dependencies
------------
[CouchDB](http://couchdb.apache.org/)

* [couchdb-lucene v0.4](http://github.com/rnewson/couchdb-lucene/tree/v0.4)
* [couchapp](http://github.com/couchapp/couchapp)

[Python](http://www.python.org/)

* [couchdb-python](http://code.google.com/p/couchdb-python/)
* [scrapy](http://scrapy.org/)

Optionally for [Yammer](http://yammer.com) spidering:

* [pyopenssl](http://pypi.python.org/pypi/pyOpenSSL)
* [oauth](http://code.google.com/p/oauth/)

Installation
------------

Assuming couchdb-lucene was installed to the "_fti" endpoint, you can push 
Couch Crawler to your CouchDB instance with the command:

    cd couchapp
    couchapp push

This will create a new CouchDB database called "crawler" on the localhost:5984 
CouchDB instance. To change the db, modify couchapp/.couchapprc and do another
couchapp push.

To configure the crawler, copy python/couchcrawler-sample.cfg to python/couchcrawler.cfg and fill out the appropriate configuration values. 

To start indexing pages, run the crawler script:

    cd python
    ./scrapy-ctl.py crawl domain_to_crawl.com

While it's indexing, you can visit the search engine at the following url:

  http://localhost:5984/crawler/_design/crawler/index.html
  
Spiders
-------
The crawler current has spiders for:

* MediaWiki
* Twiki
* Yammer

It's pretty easy to create your own. See python/couchcrawler/spiders/wiki.py for an example, or [Scrapy documentation](http://doc.scrapy.org/intro/tutorial.html) for more a more in-depth explanation.

