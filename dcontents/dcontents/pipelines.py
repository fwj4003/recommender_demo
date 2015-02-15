# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors


class DcontentsPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
        		host='127.0.0.1',
                db = 'douban',
                user = 'root',
                passwd = 'pikachu',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self,tx,item):
        feature=classification=actor=''
        lenClassification=len(item['classification'])
        lenActor=len(item['actor'])
        lenFeature=len(item['feature'])
        for n in xrange(lenClassification):
            classification+=item['classification'][n]
            if n<lenClassification-1:
                classification+='/'
        for n in xrange(lenActor):
            actor+=item['actor'][n]
            if n<lenActor-1:
                actor+='/'
        for n in xrange(lenFeature):
            feature+=item['feature'][n]
            if n<lenFeature-1:
                feature+='/'
        id = item['id'][0]
        title = ''
        if item['title']:
            title = item['title'][0]
        year = ''
        if item['year']:
            year=item['year'][0]
        score = ''
        if item['score']:
            score = item['score'][0]
        director = ''
        if item['director']:
            director = item['director'][0]
        tx.execute(\
            "insert into contents (id,title,year,score,director,classification,actor,feature) values (%s,%s,%s,%s,%s,%s,%s,%s)",\
            (id,title,year,score,director,classification,actor,feature))
        ##log.msg("Item stored in db: %s" % item, level=log.DEBUG)
        log.msg("Item stored in db : %s" % item['id'],level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)