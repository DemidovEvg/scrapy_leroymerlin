# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from .spiders.leroymerlin import leroymerlinSpider
from scrapy.pipelines.images import ImagesPipeline
import re


class LeroymerlinProjectPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.leroymerlin
        self.db[leroymerlinSpider.name].drop()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        del item['path_for_photo']
        collection.update_one(item, {'$set': item}, upsert=True) 
        return item

class LeroymerlinProjectPipelinePhoto(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['product_photos']:
            for img in item['product_photos']:
                try:
                    yield scrapy.Request(img)
                except  Exception as e:
                    print(e)
        return super().get_media_requests(item, info)

    def item_completed(self, results, item, info):
        num_dict_in_result = 1
        for i in range(len(results)):
            item['product_photos'][i] = results[i][num_dict_in_result]['path']
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        path = super().file_path(request, response, info, item=item)
        path = path.replace('full/', '')
        path = f"{item['path_for_photo']}{path}"
        return path

