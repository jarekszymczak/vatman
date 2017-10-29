import os

import scrapy

from commons.config import ALLEGRO_ITEMS_DIRECTORY, ALLEGRO_USERS_DIRECTORY, CATEGORIES_URL


class AllegroListingSpider(scrapy.Spider):
    name = "allegro"

    def start_requests(self):
        urls = []

        for category_url in CATEGORIES_URL:
            urls.append(category_url)
            urls.extend(
                category_url + '&p={}'.format(i) for i in
                range(2, 1001))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_listing)

    @staticmethod
    def dump_html(response, output_path):
        with open(output_path, 'w') as f:
            f.write(response.body.decode("utf-8"))

    @staticmethod
    def item_output_path(url):
        return os.path.join(ALLEGRO_ITEMS_DIRECTORY, url.split("/")[-1].split('?')[0])

    @staticmethod
    def user_output_path(url):
        return os.path.join(ALLEGRO_USERS_DIRECTORY, url.split("/")[-2])

    def parse_listing(self, response):
        item_links = response.css('._342830a > a::attr(href)').extract()
        for url in item_links:
            if not os.path.exists(self.item_output_path(url)):
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        self.dump_html(response, self.item_output_path(response.url))
        user_link = response.css('.btn-user > a.alleLink::attr(href)').extract()
        if len(user_link) != 1:
            raise Exception('Wrong identification of user link')

        for a in user_link:
            url = 'http://allegro.pl' + a.replace('uzytkownik', 'sellerInfoFrontend').replace('oceny', 'aboutSeller')
            if not os.path.exists(self.user_output_path(url)):
                yield scrapy.Request(url, callback=self.parse_user)

    def parse_user(self, response):
        self.dump_html(response, self.user_output_path(response.url))
