#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#=============================================================================
#     FileName: conf.py
#         Desc: 
#       Author: lizherui
#        Email: lzrak47m4a1@gmail.com
#     HomePage: https://github.com/lizherui
#      Version: 0.0.1
#   LastChange: 2013-04-07 14:48:26
#      History:
#=============================================================================
'''

import os

#项目路径
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

#配置路径
CONF_PATH = PROJECT_PATH + '/conf'

#数据路径
DATA_PATH = PROJECT_PATH + '/data'

#输出文件路径
EXPORT_PATH = PROJECT_PATH + '/export'

#微博主题路径
MICRO_BLOG = DATA_PATH +'/micro_blog_sort.txt'

#用户黑名单文件
USER_BLACKLIST_FILE = EXPORT_PATH + '/user_blacklist.txt'

#微博内容黑名单文件
BLOG_BLACKLIST_FILE = EXPORT_PATH + '/blog_blacklist.txt'

#微博长度文件
BLOG_LENGTH_FILE = EXPORT_PATH + '/blog_length.txt'

#微博长度统计文件
BLOG_LENGTH_STATS_FILE = EXPORT_PATH + '/blog_length_stats.txt'

#用户发微博总数的文件
USER_TOTAL_BLOGS_FILE = EXPORT_PATH + '/user_total_blogs.txt'

#每个用户每天发的微博数量
USER_EVERYDAY_BLOGS_FILE = EXPORT_PATH + '/user_everyday_blogs.txt'

#每个用户每天发的微博数量的统计数据
USER_EVERYDAY_BLOGS_STATS_FILE = EXPORT_PATH + '/user_everyday_blogs_stats.txt'

#每个用户每天发的垃圾微博数量
USER_EVERYDAY_TRASH_BLOGS_FILE = EXPORT_PATH + '/user_everyday_trash_blogs.txt'

#每个用户每天发的垃圾微博数量的统计数据
USER_EVERYDAY_TRASH_BLOGS_STATS_FILE = EXPORT_PATH + '/user_everyday_trash_blogs_stats.txt'

#文件中列与列的分隔符
FILE_SPLIT_STRING = '|!|'

#每一行内容分割后用户名的数组下标
USER_NAME_INDEX = 3

#每一行内容分割后用户昵称的数组下标
USER_NICKNAME_INDEX = 4

#每一行内容分割后微博内容的数组下标
BLOG_CONTENT_INDEX = 6

#每一行内容分割后发布时间的数组下标
PUBLISH_TIME_INDEX = 8

#中策略情况下，同一个用户连续发布的微博最大数量
STRATEGY_NUM = 15

#中策略情况下，一定微博数量的头尾相差最长时间, 以秒为单位
STRATEGY_TIME = 30
