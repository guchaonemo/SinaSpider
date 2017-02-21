#! /usr/bin/env python2.7
# -*- coding:utf-8-*-
# -*- coding: cp936 -*-
# -*- coding: gb18030 -*-


#--------------------------------------------------#
#     Author:guchao
#     mail  :guchaonemo@163.com
#     time  :2017.2.18 15:00
#     USAEG :python crawl
#--------------------------------------------------#
import re
from scrapy.spider import CrawlSpider
from SinaSpider.weiboID import weiboID
from scrapy.http import Request
from SinaSpider.items import InformationItem
from bs4 import BeautifulSoup
import sys
import time
import warnings
warnings.filterwarnings("ignore")


reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(CrawlSpider):
    name = "SinaSpider"
    host = "http://weibo.com"
    start_urls = []
    weiboIDs = weiboID()
    for ID in weiboIDs:
        url = "http://weibo.com/u/%s?is_all=1" % ID
        start_urls.append(url)
    # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, method='GET', callback=self.parse)

    def parse(self, response):
        informationItems = InformationItem()
        content = response.body
        soup = BeautifulSoup(content, 'html.parser')
        result = soup.find_all('span', class_="pic_box")
        otherIDS = []
        for each in result:
            try:
                usercard = each.a.img['usercard']
                otherIDS.append(str(re.findall('id=(.*?)&', usercard)[0]))
            except:
                pass
        ID = re.findall('CONFIG\[\'oid\'\]=\'(.*?)\';', content)
        nickname = re.findall('CONFIG\[\'onick\'\]=\'(.*?)\';', content)
        informationItems["URL"] = response.url
        if nickname:
            informationItems["NickName"] = nickname[0]
        if ID:
            informationItems["uid"] = ID[0]
            self.finish_ID = self.finish_ID | set(str(ID[0]))
        fGender = soup.find_all('i', class_='W_icon icon_pf_female')
        if fGender:
            informationItems["Gender"] = "fmale"
        else:
            informationItems["Gender"] = "male"
        Tweets = soup.find_all('strong')
        if len(Tweets) >= 3:
            informationItems['Num_Follows'] = (Tweets[0].string)
            informationItems['Num_Fans'] = (Tweets[1].string)
            informationItems['Num_Tweets'] = (Tweets[2].string)
        yield informationItems
        '''if nickname:
            informationItems["NickName"] = nickname[0]
        if gender:
            informationItems["Gender"] = gender[0]
        if place:
            place = place[0].split(" ")
            informationItems["Province"] = place[0]
            if len(place) > 1:
                informationItems["City"] = place[1]
        if signature:
            informationItems["Signature"] = signature[0]
        if birthday:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                informationItems["Birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception:
                pass
        if sexorientation:
            if sexorientation[0] == gender[0]:
                informationItems["Sex_Orientation"] = "gay"
            else:
                informationItems["Sex_Orientation"] = "Heterosexual"
        if marriage:
            informationItems["Marriage"] = marriage[0]
        '''

        '''urlothers = "http://weibo.cn/attgroup/opening?uid=%s" % ID
        r = requests.get(urlothers, cookies=response.request.cookies)
        if r.status_code == 200:
            selector = etree.HTML(r.content)
            texts = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
            if texts:
                num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', texts)  # 微博数
                num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', texts)  # 关注数
                num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', texts)  # 粉丝数
                if num_tweets:
                    informationItems["Num_Tweets"] = int(num_tweets[0])
                if num_follows:
                    informationItems["Num_Follows"] = int(num_follows[0])
                if num_fans:
                    informationItems["Num_Fans"] = int(num_fans[0])
        yield informationItems'''
        for ID in otherIDS:
            url = "http://weibo.com/u/%s?is_all=1" % ID
            if set(str(ID)) not in self.finish_ID:
                self.finish_ID = self.finish_ID | set(str(ID))
                yield Request(url=url, method='GET', callback=self.parse)
