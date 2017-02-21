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
import random
from user_agents import agents


class UserAgentMiddleware(object):

    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.meta['proxy'] = "http://%s" % agent
