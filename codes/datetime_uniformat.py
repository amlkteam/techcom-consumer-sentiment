# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 19:45:50 2020

@author: gen80
"""
import time
import datetime
import re

def get_uniform_date(from_snippet):
    created_at = None    
    from_str = str(from_snippet)
    d = datetime.datetime.now()
    ## 7 date formats altogeher in Weibo tweets, need to deal with each to get a uniform date:
    ## 16分钟前|4小时前| 刚刚 |昨天 04:17| 2月3日 | 02-19 | 2019-11-05
    
    #format: 刚刚(Just now)
    if re.findall("刚刚",from_str):
        return d.strftime("%Y-%m-%d %H:%M:%S")    
    # format: 16分钟(minutes)前(ago)
    elif re.findall("(\d{1,2})分钟前",from_str): 
        min_dif = int(re.findall("(\d{1,2})分钟前",from_str)[0])
        time_obj = d - datetime.timedelta(minutes=min_dif)        
    # format: 2小时(hours)前(ago)
    elif re.findall("(\d{1,2})小时前",from_str):
        hr_dif = int(re.findall("(\d{1,2})小时前",from_str)[0])
        time_obj = d - datetime.timedelta(hours=hr_dif) 
    #format: 昨天(yesterday) 04:17
    elif re.findall("(昨天 (\d{2}):(\d{2}))",from_str):
        date_ch,h,m = re.findall("(昨天 (\d{2}):(\d{2}))",from_str)[0]
        date_obj = d - datetime.timedelta(days=1)
        time_obj = date_obj.replace(hour = int(h), minute = int(m))
    #format:  2019-11-05
    elif re.findall("(\d{4})-(\d{2})-(\d{2})",from_str): 
        year, month, day =re.findall("(\d{4})-(\d{2})-(\d{2})",from_str)[0]
        time_obj = d.replace(year = int(year), month=int(month),day=int(day))
    #format: 02-19
    elif re.findall("(\d{2})-(\d{2})",from_str): 
        month, day =re.findall("(\d{2})-(\d{2})",from_str)[0]
        time_obj =d.replace(month=int(month),day=int(day))
    #format: 2月(Month)3日(Day)    
    elif re.findall("((\d+)月(\d+)日)",from_str):
        date_ch, month,day = re.findall("((\d+)月(\d+)日)",from_str)[0]
        t_obj = time.strptime(date_ch, "%m月%d日")
        return time.strftime("%Y-%m-%d %M:%S",t_obj).replace('1900','2020')
    
    created_at = time_obj.strftime("%Y-%m-%d %H:%M:%S")
    return created_at