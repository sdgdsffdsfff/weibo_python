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

#输出的用户名黑名单路径
USERNAME_BLACKLIST_FILE = EXPORT_PATH + '/username_blacklist.txt'

#输出的微博内容黑名单路径
WEIBO_CONTENT_BLACKLIST_FILE = EXPORT_PATH + '/weibo_content_blacklist.txt'

#每一行内容分割后用户名的数组下标
USER_NAME_INDEX = 3

#每一行内容分割后用户昵称的数组下标
USER_NICKNAME_INDEX = 4

#每一行内容分割后微博内容的数组下标
WEIBO_CONTENT_INDEX = 6

#每一行内容分割后发布时间的数组下标
PUBLISH_TIME_INDEX = 8

#中策略情况下，同一个用户连续发布的微博最大数量
STRATEGY_NUM = 15

#中策略情况下，一定微博数量的头尾相差最长时间, 以秒为单位
STRATEGY_TIME = 30
