# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class A51JobPipeline(object):


    def open_spider(self,spider):
        # 连接mongodb
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        # 选数据库
        self.db = self.client.job
        # 选集合
        self.table = self.db.content
        #删除全部数据
        try:
            self.table.remove({})
        except Exception:
            pass

    def process_item(self, item, spider):
        # 把item转换为字典类型
        text = dict(item)
        # 写入数据    
        self.table.insert(text)
        return item

    def close_spider(self,spider):
        self.client.close()