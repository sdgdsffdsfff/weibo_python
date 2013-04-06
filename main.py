#coding=utf-8
import sys
import os
import time
from conf.conf import *

dict_global_variable = {} #全局变量字典
dict_user_blacklist = {} #垃圾用户黑名单
dict_blog_blacklist = {} #垃圾微博黑名单
dict_username_time = {} #记录每个用户连续发出的一定数量的每条微博的时间
dict_username_usernickname = {} #记录用户名和用户昵称的映射关系
dict_blog_length = {} #记录所有微博的长度
dict_blog_length_stats = dict(average = 0, variance = 1) #所有微博长度的统计文件
dict_user_total_blogs = {} #记录每个用户所发微博的总数量
dict_user_everyday_blogs = {} #记录每个用户每天发的微博数量
dict_user_everyday_blogs_stats = {} #每个用户每天发的微博数量的统计数据
dict_user_everyday_trash_blogs = {} #记录每个用户每天发的垃圾微博数量
dict_user_everyday_trash_blogs_stats = {} #记录每个用户每天发的垃圾微博数量
set_dates = set()

#将时间格式转化为unix时间戳
def date_time2unix_time(str_time):
    arr1 = map(lambda x : int(x), (str_time.split(' '))[0].split('-'))
    arr2 = map(lambda x : int(x), (str_time.split(' '))[1].split(':'))
    arr_time = arr1 + arr2  + [0] * 3
    return int(time.mktime(arr_time))

#把数据输出到文件
def datas2file(input_data):
    dict_data, str_filename = input_data[0], input_data[1]
    f = open(str_filename, 'w')
    if str_filename == BLOG_LENGTH_STATS_FILE:
        f.write(str(dict_data['average']) + FILE_SPLIT_STRING + str(dict_data['variance']) + '\n')
    elif str_filename in (USER_EVERYDAY_BLOGS_FILE, USER_EVERYDAY_TRASH_BLOGS_FILE):
        for str_user_name, dict_everyday_blogs in dict_data.iteritems():
            tuple_data = sorted(dict_everyday_blogs.items(), key=lambda d: d[0])
            f.write(FILE_SPLIT_STRING.join((str_user_name, dict_username_usernickname[str_user_name])))
            for date, blogs in tuple_data:
                f.write(FILE_SPLIT_STRING + date + "," + str(blogs))
            f.write('\n')
    elif str_filename in (USER_EVERYDAY_BLOGS_STATS_FILE, USER_EVERYDAY_TRASH_BLOGS_STATS_FILE):
        tuple_data = sorted(dict_data.items(), key = lambda d: d[1]['average'], reverse = True)
        for uname, stats in tuple_data:
            f.write(FILE_SPLIT_STRING.join((uname, dict_username_usernickname[uname], str(stats['with_zero_average']), \
                    str(stats['with_zero_variance']), str(stats['average']), str(stats['variance']))) + '\n')
    else:
        tuple_data = sorted(dict_data.items(), key = lambda d: d[1], reverse = True)
        for data_name, data_num in tuple_data:
            if str_filename == USER_BLACKLIST_FILE:
                f.write(FILE_SPLIT_STRING.join((data_name, dict_username_usernickname[data_name], str(data_num))) + '\n')
            elif str_filename in (BLOG_BLACKLIST_FILE, BLOG_LENGTH_FILE):
                f.write(FILE_SPLIT_STRING.join((data_name, str(data_num))) + '\n')
            elif str_filename == USER_TOTAL_BLOGS_FILE:
                f.write(FILE_SPLIT_STRING.join((data_name, dict_username_usernickname[data_name],
                    str(data_num), str(float(data_num) / dict_global_variable['total_blogs'] * 100) + '%')) + '\n')
            else:
                pass
    f.close()

#计算均值和方差
def calculate_average_and_variance(arr):
    average_value = sum(arr) / len(arr)
    variance_value = sum((value - average_value) ** 2 for value in arr) ** 0.5
    return average_value, variance_value

#将数据从dict类型转化为统计用的list类型
def stats_dict2list(di):
    arr = []
    for key in di:
        arr += [int(key)] * di[key]
    return arr


def main():

    blog_file = open(MICRO_BLOG, 'r')
    arr_blogs = blog_file.readlines()
    dict_global_variable['total_blogs'] = len(arr_blogs)

    for str_line in arr_blogs:
        arr_line = str_line.split(FILE_SPLIT_STRING)
        str_user_name = arr_line[USER_NAME_INDEX]
        str_user_nickname = arr_line[USER_NICKNAME_INDEX]
        str_blog_content = arr_line[BLOG_CONTENT_INDEX]
        str_date = arr_line[PUBLISH_TIME_INDEX].split(" ")[0]
        int_publish_time = date_time2unix_time(arr_line[PUBLISH_TIME_INDEX])
        str_blog_length = str(len(str_blog_content) / 3)
        set_dates.add(str_date)

        #建立用户名和用户昵称的映射表
        if str_user_name not in dict_username_usernickname:
            dict_username_usernickname[str_user_name] = str_user_nickname

        #记录每个用户所发的微博数量
        dict_user_total_blogs[str_user_name] = dict_user_total_blogs.get(str_user_name, 0) + 1

        #记录微博长度
        dict_blog_length[str_blog_length] = dict_blog_length.get(str_blog_length, 0) + 1
        
        #记录每个用户每天发的微博数量
        dict_user_everyday_blogs[str_user_name] = dict_user_everyday_blogs.get(str_user_name, {})
        dict_user_everyday_blogs[str_user_name][str_date] = dict_user_everyday_blogs[str_user_name].get(str_date, 0) + 1

        #用滑动窗口技术判断用户发微博是否命中策略
        dict_username_time[str_user_name] = dict_username_time.get(str_user_name, [])
        dict_username_time[str_user_name].append(dict(content = str_blog_content, time = int_publish_time))
        if len(dict_username_time[str_user_name]) < STRATEGY_NUM:
            continue
        if len(dict_username_time[str_user_name]) > STRATEGY_NUM:
            del dict_username_time[str_user_name][0]
        #用户发布微博命中策略
        if dict_username_time[str_user_name][-1]['time'] - dict_username_time[str_user_name][0]['time'] <= STRATEGY_TIME:
            dict_user_everyday_trash_blogs[str_user_name] = dict_user_everyday_trash_blogs.get(str_user_name, {})
            dict_user_everyday_trash_blogs[str_user_name][str_date] = dict_user_everyday_trash_blogs[str_user_name].get(str_date, 0) + STRATEGY_NUM
            #每次命中策略，每条垃圾微博只算命中一次，所以需要去重处理
            set_content_temp = set()
            for blog_data in dict_username_time[str_user_name]:
                set_content_temp.add(blog_data['content'])
            for content in set_content_temp:
                dict_blog_blacklist[content] = dict_blog_blacklist.get(content, 0) + 1
            dict_user_blacklist[str_user_name] = dict_user_blacklist.get(str_user_name, 0) + 1
            #清空处理
            dict_username_time[str_user_name] = []

    dict_global_variable['total_dates'] = len(set_dates)
    #均值和方差的统计处理
    dict_blog_length_stats['average'], dict_blog_length_stats['variance'] = calculate_average_and_variance(stats_dict2list(dict_blog_length))
    stats_input = (
        (dict_user_everyday_blogs, dict_user_everyday_blogs_stats),
        (dict_user_everyday_trash_blogs, dict_user_everyday_trash_blogs_stats),
    )
    for datas in stats_input:
        dict_raw, dict_stats = datas[0], datas[1]
        for key_uname, value_blogs in dict_raw.iteritems(): 
            dict_stats[key_uname] = dict(average = 0, variance = 1, with_zero_average = 0, with_zero_variance = 1)
            dict_stats[key_uname]['average'], dict_stats[key_uname]['variance'] = \
                    calculate_average_and_variance([num for date, num in value_blogs.iteritems()])
            dict_stats[key_uname]['with_zero_average'], dict_stats[key_uname]['with_zero_variance'] = \
                    calculate_average_and_variance([num for date, num in value_blogs.iteritems()] + \
                    [0] * (dict_global_variable['total_dates'] - len(value_blogs)))

    #输出到文件
    input_datas = (
        (dict_user_blacklist, USER_BLACKLIST_FILE),
        (dict_blog_blacklist, BLOG_BLACKLIST_FILE),
        (dict_blog_length, BLOG_LENGTH_FILE),
        (dict_blog_length_stats, BLOG_LENGTH_STATS_FILE),
        (dict_user_total_blogs, USER_TOTAL_BLOGS_FILE),
        (dict_user_everyday_blogs, USER_EVERYDAY_BLOGS_FILE),
        (dict_user_everyday_blogs_stats, USER_EVERYDAY_BLOGS_STATS_FILE),
        (dict_user_everyday_trash_blogs, USER_EVERYDAY_TRASH_BLOGS_FILE),
        (dict_user_everyday_trash_blogs_stats, USER_EVERYDAY_TRASH_BLOGS_STATS_FILE),
    )
    for input_data in input_datas:
        datas2file(input_data)

    blog_file.close()

if __name__ == '__main__':
    main()
