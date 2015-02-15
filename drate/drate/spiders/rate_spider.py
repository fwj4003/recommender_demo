__author__ = 'shiyuan'
 # -*- coding: UTF-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from drate.items import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class RateSpider(CrawlSpider):
    name = "douban_rate"
    allowed_domains = ["movie.douban.com"]
    start_urls = []
    f = file("drama.json")
    jobj = json.load(f)
    pre_url = u'http://movie.douban.com/subject/'
    end_url = u'/comments?start=0&limit=20&sort=time'
    for data in jobj:
        start_urls.append(pre_url+data['id']+end_url)
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+/comments\?start=\d+&limit=20&sort=time')),follow=True,callback="parse_item"),
    ]

    def parse_item(self,response):
        item = DrateItem()
        sel = Selector(response)
        id = (response.url).split('/')[-2:-1]
        user = sel.xpath('//*[@id="comments"]//span[@class="comment-info"]/a/@href').extract()
        rate = sel.xpath('//*[@id="comments"]//span[@class="comment-info"]/span/@title').extract()
        score = []
        mp = {
            u'力荐': '5',
            u'推荐': '4',
            u'还行': '3',
            u'较差': '2',
            u'很差': '1'}
        for i in rate:
            score.append(mp[i])
        aid=[]
        for i in user:
            aid.append(i.split('/')[-2:-1][0])
        item['id']=id
        item['score']=score
        item['aid']=aid
        return item
