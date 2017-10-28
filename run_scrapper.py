from scrapy.crawler import CrawlerProcess

from scraper.allegro.allegro_listings import AllegroListingSpider

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(AllegroListingSpider())
    process.start()  # the script will block here until the crawling is finished