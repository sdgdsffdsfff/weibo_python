#coding=utf-8
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
MICRO_BLOG = DATA_PATH + '/MICRO_BLOG.txt'

#关键词黑名单路径
WORDS_BLACKLIST = CONF_PATH + '/words_blacklist'

#微博评论路径
MICRO_BLOG_COMMENT = DATA_PATH + '/MICRO_BLOG_COMMENT.txt'

#输出的用户名黑名单路径
USERNAME_BLACKLIST_FILE = EXPORT_PATH + '/username_blacklist.txt'

#输出的微博内容黑名单路径
WEIBO_CONTENT_BLACKLIST_FILE = EXPORT_PATH + '/weibo_content_blacklist.txt'

#每一行内容分割后用户名的数组下标
USERNAME_INDEX = 4

#每一行内容分割后微博内容的数组下标
WEIBO_CONTENT_INDEX = 6

#每一行内容分割后发布时间的数组下标
PUBLISH_TIME_INDEX = 8

#同一个用户连续发微博的最短时间限制,以秒为单位
PUBLISH_MIN_TIME = 5

#某用户中策略的次数最低限制
USER_HIT_STRATERGY_LIMIT = 50

#某微博中策略的次数最低限制
WEIBO_HIT_STRATERGY_LIMIT = 100
