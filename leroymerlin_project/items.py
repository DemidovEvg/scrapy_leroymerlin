# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
import re

def change_url(url: str):
    try:
        url = url.replace('_82', '_2000')
    except:
        pass
    return url


def str_to_int(price_str)->int:
    price_list = []
    price_str = price_str[0] if isinstance(price_str, list) else price_str
    for sal in price_str:
        if sal.isdigit():
            price_list.append(sal)
    result = int(''.join(price_list))
    if not result:
        return None
    else:
        return result

def get_specifications(specifications):
    selector = scrapy.Selector(text = specifications)
    specifications = {}
    for spec in selector.xpath('//div[@class="def-list__group"]'):
        spec_name = spec.xpath('.//dt/text()').get().strip()
        spec_value = spec.xpath('.//dd/text()').get().strip()
        specifications[spec_name] = spec_value
    return specifications

def split(url):
    path_for_photo = re.sub(r'https://.+?/', '', url)
    path_for_photo = re.sub('\/\?.+', '/', path_for_photo)
    return path_for_photo

class LeroymerlinProjectItem(scrapy.Item):
    product_name = scrapy.Field(output_processor=TakeFirst())
    product_photos = scrapy.Field(output_processor=MapCompose(change_url))
    product_url = scrapy.Field(output_processor=TakeFirst())
    product_price = scrapy.Field(input_processor=MapCompose(str_to_int), output_processor=TakeFirst())
    product_specifications = scrapy.Field(input_processor=MapCompose(get_specifications))
    path_for_photo = scrapy.Field(input_processor=MapCompose(split), output_processor=TakeFirst())

