__author__ = 'shiyuan'
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from dcontents.items import *
import json
class MoiveSpider(CrawlSpider):
    name="douban_drama"
    allowed_domains=["movie.douban.com"]
    start_urls=[]
    f=file("drama.json")
    jobj=json.load(f)
    jobj=jobj['subjects']
    for data in jobj:
        start_urls.append(data['url'])
    rules=[
        ##Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+/$')),follow=False,callback="parse_item"),
    ]

    def parse_item(self,response):
        sel=Selector(response)
        item=DcontentsItem()
        item['id']=response.url
        item['id']=item['id'].split('/')[-2:-1]
        item['title']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//a[@rel="v:starring"]/text()').extract()
        item['feature']=[]
        tmp=sel.xpath('//*[@id="content"]/div/div[2]/div[4]/div/a/text()').extract()
        if len(tmp)!=3:
            item['feature']+=tmp
        tmp=sel.xpath('//*[@id="content"]/div/div[2]/div[5]/div/a/text()').extract()
        if len(tmp)!=3:
            item['feature']+=tmp
        tmp=sel.xpath('//*[@id="content"]/div/div[2]/div[6]/div/a/text()').extract()
        if len(tmp)!=3:
            item['feature']+=tmp
        return item