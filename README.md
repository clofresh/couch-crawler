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
* [httplib2](http://code.google.com/p/httplib2/)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

Installation
------------

Assuming couchdb-lucene was installed to the "_fti" endpoint, you can push 
Couch Crawler to your CouchDB instance with the command:

    cd couchapp
    couchapp push

This will create a new CouchDB database called "crawler" on the localhost:5984 
CouchDB instance. To change the db, modify couchapp/.couchapprc and do another
couchapp push.

To start indexing pages, run the crawler script:

    cd python
    python crawler.py http://url_to_crawl1 http://url_to_crawl2 ...

The crawler will start indexing given urls and follow and index any links it 
finds. You can set the max depth to follow urls with the -d option.

While it's indexing, you can visit the search engine at the following url:

  http://localhost:5984/crawler/_design/crawler/index.html


