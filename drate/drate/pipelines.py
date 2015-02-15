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

class DratePipeline(object):
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
        tx.execute("select no from contents where id= %s",(item['id'][0],))
        no = tx.fetchone()
        no = no['no']
        l = min(len(item['aid']),len(item['score']))
        ##print '-------------------------------------'
        ##print len(item['aid'])
        ##print '-------------------------------------'
        for i in xrange(l):
            tx.execute('select * from rate where aid=%s',(item['aid'][i],))
            result = tx.fetchone()
            if result:
                pre_score = result['score']
                now_score = pre_score[0:(no-1)]+item['score'][i]+pre_score[no:]
                tx.execute('update rate set score=%s where aid=%s',(now_score,item['aid'][i]))
            else:
                now_score = (no-1)*'0'+item['score'][i]+(500-no)*'0'
                tx.execute('insert into rate (aid,score) values (%s,%s)',(item['aid'][i],now_score))
        ##log.msg("Item stored in db: %s" % item, level=log.DEBUG)
        log.msg("Item stored in db : %s" % item['id'],level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)