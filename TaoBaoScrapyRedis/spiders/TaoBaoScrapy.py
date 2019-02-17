# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from urllib.parse import quote
from TaoBaoScrapyRedis.items import TaobaoItemLoader, TaobaoscrapyredisItem
from selenium import webdriver
from pydispatch import dispatcher
from scrapy import signals
from TaoBaoScrapyRedis.utils import register
from scrapy.selector import csstranslator

class TaobaoscrapySpider(RedisSpider):
    name = 'TaoBaoScrapy'
    allowed_domains = ['taobao.com']
    redis_key = 'TaoBaoScrapy:start_url'

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
        super(TaobaoscrapySpider, self).__init__()
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def spider_close(self, spider):
        """
        当爬虫退出的时候关闭Chrome
        :param spider:
        :return:
        """
        print("spider closed")
        self.browser.quit()

    def start_requests(self):
        headers = {
            "Host": "ws.mmstat.com",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Key": "XuEbXy+hbO12vlD5okm2pw==",
            "Sec-WebSocket-Version": "13",
            "Upgrade": "websocket",
            "Origin": " https://s.taobao.com",
            "Connection": "Upgrade",
            "Cache-Control": "no-cache",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.browser, list = register()
        base_url = 'https://s.taobao.com/search?q='
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = base_url + quote(keyword) + '&s='+str(page*44)
                yield Request(url=url, headers=headers, callback=self.parse, dont_filter=True, cookies=list)

    def parse(self, response):
        lists = response.css('.mainsrp-itemlist .m-itemlist .grid g-clearfix div:first-child')
        for list in lists:
            item_loader = TaobaoItemLoader(item=TaobaoscrapyredisItem(), response=list)
            item_loader.add_css('url', 'a[class="pic-link J_ClickStat J_ItemPicA"]::attr(htef)')
            item_loader.add_css('price', 'div[class="price g_price g_price-highlight"] strong::text')
            item_loader.add_css('image', 'a[class="pic-link J_ClickStat J_ItemPicA"] img::attr(src)')
            item_loader.add_css('buy', 'div[class="deal-cnt"]::text')
            item_loader.add_css('shop', 'div[class="shop"] a span::nth-child(2)::text')
            item_loader.add_css('shop_url', 'div[class="shop"] a::attr(href)')
            item_loader.add_css('location', 'div[class="location"]::text')
            item_loader.add_css('dsec', 'div[class="row row-2 title"] a::text')

            return item_loader.load_item()
