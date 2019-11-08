import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.imdb.com/lists/tt0074486?ref_=tt_rls_sm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.list-preview'):
            yield {
                '==NAME==': quote.css('div.list_name a::text').get(),
                '==META==': quote.css('div.list_meta::text').get()
            }