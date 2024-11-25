import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        # Извлекаем все блоки с книгами
        books = response.css('article.product_pod')

        for book in books:
            # Извлекаем название, цену, рейтинг и ссылку на книгу
            title = book.css('h3 a::attr(title)').get()
            price = book.css('p.price_color::text').get()
            rating = book.css('p.star-rating::attr(class)').get().split()[-1]  # Рейтинг книги
            link = book.css('h3 a::attr(href)').get()

            # Выводим данные
            yield {
                'title': title,
                'price': price,
                'rating': rating,
                'link': response.urljoin(link),
            }

        # Если есть следующая страница, переходим на нее
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
