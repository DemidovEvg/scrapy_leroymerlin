import scrapy
import re
from scrapy.http import HtmlResponse
from ..items import LeroymerlinProjectItem
from scrapy.loader import ItemLoader
from ..items import LeroymerlinProjectItem


class leroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_page_num = 1
    # Ноутбуки в Санкт-Петербурге Apple от 30т 
    #  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls
        for url_sub_path in kwargs['url_sub_paths']:
            self.start_urls.append(f"https://spb.leroymerlin.ru/catalogue/{url_sub_path}")

    def page_switcher(self, url):
        self.start_page_num +=1
        if 'page=' in url:
            url = re.sub(r'page=\d+', f'page={self.start_page_num}', url)
        else:
            url = f'{url}?page={self.start_page_num}'
        return url

    def parse(self, response: HtmlResponse):
        products = response.xpath("//a[contains(@href, '/product/') and contains(@data-qa, 'product-image')]")

        if not products:
            return

        for product in products:
            yield response.follow(product, callback=self.product_parse, cb_kwargs={'path_for_photo': response.url})

        next_page = self.page_switcher(response.url) 
        yield response.follow(next_page, callback=self.parse)
    
    def product_parse(self, response: HtmlResponse, **kwargs):
        product = ItemLoader(item=LeroymerlinProjectItem(), response=response)
        product.add_xpath('product_name', '//h1/text()')
        product.add_xpath('product_photos', '//img[@slot="thumbs"]/@src')
        product.add_value('product_url', response.url)
        product.add_xpath('product_price', "//span[@slot='price']/text()")
        product.add_xpath('product_specifications', "//dl[@class='def-list']")
        product.add_value('path_for_photo', kwargs['path_for_photo'])
        return product.load_item()


