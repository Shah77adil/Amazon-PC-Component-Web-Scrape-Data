import scrapy

from scrapy.exceptions import CloseSpider

class CpuSpider(scrapy.Spider):
    name = 'cpu_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=cpu']

    # Custom settings
    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # Delay between requests to prevent getting blocked
        'CONCURRENT_REQUESTS': 2,  # Number of concurrent requests
        'RETRY_TIMES': 5,  # Number of retries for failed requests
        'RETRY_HTTP_CODES': [503, 502, 504, 408],  # HTTP codes to retry
    }

    def parse(self, response):
        # Check for 503 Service Unavailable
        if response.status == 503:
            self.logger.error("Received 503 Service Unavailable. Retrying...")
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
            return

        # Extracting product information
        products = response.css('div.s-main-slot div.s-result-item')

        if not products:
            self.logger.warning("No products found on this page.")
            raise CloseSpider("No products found")

        for product in products:
            title = product.css('h2 a span::text').get()
            price = product.css('span.a-price span.a-offscreen::text').get()
            link = product.css('h2 a::attr(href)').get()
            if link:
                link = response.urljoin(link)

            if title and price and link:
                
                yield {
                    'title': title,
                    'price': price,
                    'link': link,
                }
        
        # Handling pagination
        next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("No more pages to scrape.")

# To run this spider, use the command:
# scrapy crawl cpu_spider -o output.json
