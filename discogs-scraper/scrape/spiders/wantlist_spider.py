import scrapy
from scrapy.http import Request
from scrape import settings
from scrapy.http.cookies import CookieJar

from scrape.items import DiscogsRecord, DiscogsSeller

import re

class WantlistSpider(scrapy.Spider):
    name = 'wantlist'
    start_urls = ['https://www.discogs.com/login?nologin=1&return_to=%2Fsell%2Fmywants?limit=500']

    def parse(self, response):
        req = scrapy.FormRequest.from_response(
            response,
            formnumber=1,
            formdata={
                'username': settings.DISCOGS_USERNAME,
                'password': settings.DISCOGS_PASSWORD,
                'Action.Login': ''
            },
            callback=self.after_login
        )

        return req

    def after_login(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        # check login succeed before going on
        if "Marketplace" not in response.body:
            scrapy.log.msg("Login failed", level=log.ERROR)
            return

        for idx, sel in enumerate(response.xpath('//table[contains(@class, "mpitems")]/tbody/tr')):
            try:
                record = DiscogsRecord()
                descXpath = sel.xpath('td[@class="item_description"]')
                record['title'] = descXpath.xpath('span[@class="br_item_title"]/a/text()').extract()[0].strip()

                info = sel.xpath('td[@class="item_description"]/text()').extract()
                record['catNum'] = info[6].strip()
                record['mediaCondition'] = info[8].strip()
                record['sleeveCondition'] = info[10].strip()
                record['sellerNotes'] = info[11].strip()
                record['label'] = sel.xpath('td[@class="item_description"]/a/text()').extract()[0].strip()

                sellerXpath = sel.xpath('.//td[@class=" seller_info"]')
                discogsSeller = DiscogsSeller()

                sellerInfo = sellerXpath.xpath('ul/li/b/a/text()').extract()

                discogsSeller['name'] = record['seller'] = sellerInfo[0].strip()

                if len(sellerInfo) > 1:
                    p = re.compile(r'.*(\d+).*')
                    m = p.match(sellerInfo[1].strip())
                    discogsSeller['numItems'] = int(m.group(1))
                else:
                    discogsSeller['numItems'] = 0

                discogsSeller['country'] = filter(lambda x : len(x) != 0, [x.strip() for x in sellerXpath.xpath('ul/li/text()').extract()])[0]

                priceXpath = sel.xpath('.//td[@align="center"]')
                record['price'] = priceXpath.xpath('span[@class="price"]/text()').extract()[0]
                record['shipping'] = priceXpath.xpath('span[@style="color:#555"]/text()').extract()[0].strip()

                yield discogsSeller
                yield record
            except:
                print "index %d" % idx
                print sel

                from scrapy.shell import inspect_response
                inspect_response(response)

                raise