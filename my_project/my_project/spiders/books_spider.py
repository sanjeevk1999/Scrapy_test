import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            'http://books.toscrape.com/catalogue/category/books_1/page-1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'books-%s.html' % page

        for book in response.css("article.product_pod"):
            image_url = book.css("div.image_container a img::attr(src)").get()
            image_url = image_url[6:]
            book_title = book.css("h3 a::attr(title)").get()
            book_title = book_title.replace(",", "")
            book_title = book_title.replace("  ", " ")
            product_price = book.css("p.price_color::text").get()

            yield {
                "image_url":image_url,
                "book_title":book_title,
                "product_price":product_price
            }

        next_page = response.css('li.next a::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
