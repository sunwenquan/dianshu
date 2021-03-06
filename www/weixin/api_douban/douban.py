#-*- coding:utf-8 -*-
import logging
import traceback
import simplejson
import os
import sys

_lib_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_home = os.path.normpath(_lib_home)

if not(_lib_home in sys.path):
        sys.path.insert(0, _lib_home)


from utils.request import HttpRequest
from utils import xmljson
from utils import log

class RequestAPI:
	def __init__(self):
		self.hr = HttpRequest()
		self.home = 'https://api.douban.com'
		self.home_no_ssl = 'http://api.douban.com'
		self.url_search_book = 'v2/book/search'
		self.url_get_book = 'v2/book/%s'
		self.url_get_book_tag = 'v2/book/%s/tags'
		self.url_get_book_review = 'book/subject/%s/reviews'
                self.url_get_book_by_isbn = '/v2/book/isbn/%s'

	def search_books(self, keyword, tag='', offset=0, limit=1):
		_url = '%s/%s' % (self.home, self.url_search_book)
		_ret = self.hr.get(_url, {'q' : keyword, \
					   'tag' : tag, \
					   'start' : offset, \
					   'count' : limit})
		logging.debug('search book result:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book(self, id):
		_url = '%s/%s' % (self.home, self.url_get_book % id)
		_ret = self.hr.get(_url)
		logging.debug('get book restult:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book_tags(self, id):
		_url = '%s/%s' % (self.home, self.url_get_book_tag % id)
		_ret = self.hr.get(_url)
		logging.debug('get book tag result:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

	def get_book_reviews(self, id, offset=0, limit=5, orderby_time=True):
		_url = '%s/%s' % (self.home_no_ssl, self.url_get_book_review % id)
		_orderby = 'time' if orderby_time else 'score'
		_ret = self.hr.get(_url, {'start-index' : offset,\
					  'max-results' : limit,\
					  'orderby' : _orderby})
		logging.debug('get book reviews xml:%s' % _ret)
		_j_ret = xmljson.xml2json(_ret)
		logging.debug('get book reviews:%s' % _j_ret)
		return _j_ret
#		return simplejson.loads(_ret) if _ret else {} 

        def get_book_by_isbn(self, isbn):
                _url = '%s/%s' % (self.home, self.url_get_book_by_isbn % isbn)
		_ret = self.hr.get(_url)
		logging.debug('get book by isbn:%s' % _ret)
		return simplejson.loads(_ret) if _ret else {}

                
if __name__ == '__main__':
	import utils.log
	log.initlog('', True)
	rapi = RequestAPI()
#	print rapi.search_books('c')
#	print rapi.get_book(2193877)
#	print rapi.get_book_tags(2193877)
#	print rapi.get_book_reviews(2193877)
        print rapi.get_book_by_isbn('9787532706907')
	print rapi.get_book_reviews(2193877, 0, 1, False)
