from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import all the spiders
from specwise_scraper.spiders.cpu_spider import CpuSpider
from specwise_scraper.spiders.gpu_spider import GpuSpider
from specwise_scraper.spiders.ram_spider import RamSpider
from specwise_scraper.spiders.motherboard_spider import MotherboardSpider
from specwise_scraper.spiders.ssd_spider import SsdSpider
from specwise_scraper.spiders.hdd_spider import HddSpider
from specwise_scraper.spiders.power_supply_spider import PowerSupplySpider

# Start a Scrapy crawl process
process = CrawlerProcess(get_project_settings())

# List all the spiders you want to run
process.crawl(CpuSpider)
process.crawl(GpuSpider)
process.crawl(RamSpider)
process.crawl(MotherboardSpider)
process.crawl(SsdSpider)
process.crawl(HddSpider)
process.crawl(PowerSupplySpider)

# Start the crawling process and block until it's finished
process.start()
