import scrapy
from scrapy.http import Request
from scrape import settings
from scrapy.http.cookies import CookieJar

from scrape.items import DiscogsRecord

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

        for sel in response.xpath('//tbody/tr'):
            record = DiscogsRecord()
            record['title'] = sel.xpath('td/span[@class="br_item_title"]/text()').extract()
            record['label'] = sel.xpath('td/span[@class="mplabel"]/text()').extract()
            yield record