# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import MySQLdb


class SinaspiderPipeline(object):
    count = 0

    def __init__(self):
        self.ids_seen = set()
        self.conn = MySQLdb.Connect(
            host='127.0.0.1', user='root', passwd='guchao', db='wb', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            sql = '''INSERT INTO wb_uid (uid, nick, url, follows, fans, tweets, Gender) values ('%s','%s', '%s', %s, %s,  %s,'%s');''' % (
                item['uid'], item['NickName'], item['URL'], item['Num_Follows'], item['Num_Fans'], item['Num_Tweets'], item["Gender"])
            if item['uid'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item['uid'])
            else:
                self.ids_seen.add(item['uid'])
                self.cur.execute(sql)
                self.count += 1
                if self.count % 100 == 0:
                    self.conn.commit()
                return item
        except:
            pass

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
