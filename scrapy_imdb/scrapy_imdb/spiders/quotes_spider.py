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

        f= open("data_imdb.txt","w+") #create/open file for save information

        for quote in response.css('div.list-preview'): #search for all movies in the list with html's tags

            #print the results in the file
            f.write( "\n NAME: {} \n META: {}\n\n ============================= " 
            .format( quote.css('div.list_name a::text').get(),
                    quote.css('div.list_meta::text').get() ) )
            yield {
                '==NAME==': quote.css('div.list_name a::text').get(),
                '==META==': quote.css('div.list_meta::text').get()
            }
        f.close()

        #search for the next result on the next pages
        next_page = response.css('div.list-pagination a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        