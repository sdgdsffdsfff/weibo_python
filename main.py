#coding=utf-8
import sys
import os
import time
from conf.conf import *

#将时间格式转化为unix时间戳
def date_time2unix_time(str_time):
    arr1 = map(lambda x : int(x), (str_time.split(' '))[0].split('-'))
    arr2 = map(lambda x : int(x), (str_time.split(' '))[1].split(':'))
    arr_time = arr1 + arr2  + [0] * 3
    return int(time.mktime(arr_time))

def array2file(arr, filename, limit):
    f = open(filename, 'w')
    for tup in arr:
        if (tup[1] < limit):
            break
        f.write(tup[0] + ' ' + str(tup[1]) + '\n')
    f.close()

def main():
    dict_user_blacklist = {} #垃圾用户黑名单
    dict_weibo_blacklist = {} #垃圾微博黑名单
    dict_username_latesttime = {} #每个用户所发微博的最近时间戳
    arr_micro_blog = open(MICRO_BLOG, 'r').readlines()
    arr_words_blacklist = open(WORDS_BLACKLIST, 'r').readlines()

    for str_line in arr_micro_blog:
        arr_line = str_line.split('|!|')
        str_uname = arr_line[USERNAME_INDEX]
        str_weibo_content = arr_line[WEIBO_CONTENT_INDEX]
        str_publish_time = date_time2unix_time(arr_line[PUBLISH_TIME_INDEX])
                
        if 0 < str_publish_time - dict_username_latesttime.get((str_uname, str_weibo_content), 0) <= PUBLISH_MIN_TIME:
            dict_user_blacklist[str_uname] = dict_user_blacklist.get(str_uname, 0) + 1
            dict_weibo_blacklist[str_weibo_content] = dict_weibo_blacklist.get(str_weibo_content, 0) + 1
        else:
            for word in arr_words_blacklist:
                if word in str_weibo_content:
                    dict_user_blacklist[str_uname] = dict_user_blacklist.get(str_uname, 0) + 1
                    dict_weibo_blacklist[str_weibo_content] = dict_weibo_blacklist.get(str_weibo_content, 0) + 1
                    break
        dict_username_latesttime[(str_uname, str_weibo_content)] = str_publish_time


    arr_user_blacklist = sorted(dict_user_blacklist.items(), key=lambda d: d[1], reverse=True)
    arr_weibo_blacklist = sorted(dict_weibo_blacklist.items(), key=lambda d: d[1], reverse=True)

    array2file(arr_user_blacklist, USERNAME_BLACKLIST_FILE, USER_HIT_STRATERGY_LIMIT)
    array2file(arr_weibo_blacklist, WEIBO_CONTENT_BLACKLIST_FILE, WEIBO_HIT_STRATERGY_LIMIT)

if __name__ == '__main__':
    main()
