#coding=utf-8
import sys
import os
import time
from conf.conf import *

dict_user_blacklist = {} #垃圾用户黑名单
dict_weibo_blacklist = {} #垃圾微博黑名单
dict_username_time = {} #记录每个用户连续发出的一定数量的每条微博的时间
dict_username_usernickname = {} #记录用户名和用户昵称的字典

#将时间格式转化为unix时间戳
def date_time2unix_time(str_time):
    arr1 = map(lambda x : int(x), (str_time.split(' '))[0].split('-'))
    arr2 = map(lambda x : int(x), (str_time.split(' '))[1].split(':'))
    arr_time = arr1 + arr2  + [0] * 3
    return int(time.mktime(arr_time))

#把数据输出到文件
def datas2file(tuple_datas):
    for datas in tuple_datas:
        f = open(datas[1], 'w')
        for data in datas[0]:
            if datas[1] == USERNAME_BLACKLIST_FILE:
                f.write(data[0] + ' '+ dict_username_usernickname[data[0]] + ' ' + str(data[1]) + '\n')
            elif datas[1] == WEIBO_CONTENT_BLACKLIST_FILE:
                f.write(data[0] + ' ' + str(data[1]) + '\n')
            else:
                pass
        f.close()

def main():
    file_micro_blog = open(MICRO_BLOG, 'r')
    arr_micro_blog = file_micro_blog.readlines()
    for str_line in arr_micro_blog:
        arr_line = str_line.split('|!|')
        str_user_name = arr_line[USER_NAME_INDEX]
        str_user_nickname = arr_line[USER_NICKNAME_INDEX]
        str_weibo_content = arr_line[WEIBO_CONTENT_INDEX]
        int_publish_time = date_time2unix_time(arr_line[PUBLISH_TIME_INDEX])

        #建立用户名和用户昵称的映射表
        if str_user_name not in dict_username_usernickname:
            dict_username_usernickname[str_user_name] = str_user_nickname

        #用滑动窗口技术判断用户发微博是否命中策略
        dict_username_time[str_user_name] = dict_username_time.get(str_user_name, [])
        dict_username_time[str_user_name].append(dict(content = str_weibo_content, time = int_publish_time))
        if len(dict_username_time[str_user_name]) < STRATEGY_NUM:
            continue
        if len(dict_username_time[str_user_name]) > STRATEGY_NUM:
            del dict_username_time[str_user_name][0]
        #用户发布微博命中策略
        if dict_username_time[str_user_name][-1]['time'] - dict_username_time[str_user_name][0]['time'] <= STRATEGY_TIME:
            #每次命中策略，每条垃圾微博只算命中一次，所以需要去重处理
            set_content_temp = set()
            for data in dict_username_time[str_user_name]:
                set_content_temp.add(data['content'])
            for content in set_content_temp:
                dict_weibo_blacklist[content] = dict_weibo_blacklist.get(content, 0) + 1
            dict_user_blacklist[str_user_name] = dict_user_blacklist.get(str_user_name, 0) + 1
            #清空处理
            dict_username_time[str_user_name] = []

    #逆序排列黑名单
    arr_user_blacklist = sorted(dict_user_blacklist.items(), key=lambda d: d[1], reverse=True)
    arr_weibo_blacklist = sorted(dict_weibo_blacklist.items(), key=lambda d: d[1], reverse=True)

    #输出到文件
    tuple_datas = (
        (arr_user_blacklist, USERNAME_BLACKLIST_FILE),
        (arr_weibo_blacklist, WEIBO_CONTENT_BLACKLIST_FILE),
    )
    datas2file(tuple_datas)

    file_micro_blog.close()

if __name__ == '__main__':
    main()
