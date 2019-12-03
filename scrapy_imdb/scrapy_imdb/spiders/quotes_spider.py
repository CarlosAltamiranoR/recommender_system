import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # Spider's name

    def start_requests(self):
        urls = [
            'https://www.imdb.com/lists/tt0074486?ref_=tt_rls_sm' #URL to scraping
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #callback method

    def parse(self, response):      

        for quote in response.css('div.list-preview'): #search for all movies in the list with html's tags
            yield {
                '==NAME==': quote.css('div.list_name a::text').getall(),
                '==META==': quote.css('div.list_meta::text').getall(),
            }
      

        #search for the next result on the next pages
        next_page = response.css('div.list-pagination a.next-page::attr(href)').getall()        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        