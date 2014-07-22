import scrapy
from scrapy.http import Request
from scrape import settings

class WantlistSpider(scrapy.Spider):
    name = 'wantlist'
    start_urls = ['https://www.discogs.com/login?nologin=1&return=%2Fmywantlist%3F']

    def parse(self, response):
        req = scrapy.FormRequest.from_response(
            response,
            # url='https://www.discogs.com/login?nologin=1&return=%2Fmywantlist%3Fpage%3D1%26limit%3D250',
            formnumber=1,
            formdata={
                'username': settings.DISCOGS_USERNAME,
                'password': settings.DISCOGS_PASSWORD
            },
            # method='POST',
            callback=self.after_login
        )

        return req

    def after_login(self, response):
        # print response.body
        print response.request
        print response.request.body

        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)

        from scrapy.shell import inspect_response
        inspect_response(response)

        print response.xpath('//span[@class="release_title"].text()').extract()
