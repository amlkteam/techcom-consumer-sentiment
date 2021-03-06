# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:53:10 2020

@author: amy

"""

import requests
import json
import re
import pandas as pd
import time
import datetime
import sys
import urllib
import os

### extract one company each time
##manually setting the keyword for extraction because of fear of blocked access from Weibo 
#a way to deal with rate limit

keyword = "Apple"
keyword = "Amazon"
keyword = "Google"
keyword = "Microsoft"
# this does the encode transformation from Simplified Chinese names for each of tech giants
keyword = urllib.parse.quote_plus('苹果')
keyword = urllib.parse.quote_plus('亚马逊')
keyword = urllib.parse.quote_plus('谷歌')
keyword = urllib.parse.quote_plus('微软')

# simulate an browser object
temp_cookie_m = 'SSOLoginState=1583010006; ALF=1585602006; _T_WM=17082025293; XSRF-TOKEN=7ed31e; WEIBOCN_FROM=1110006030; MLOGIN=0'
browser_info_m = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
headers = {'Cookies':temp_cookie_m,
            'User-Agent': browser_info_m}

def get_cleaned_txt(txt_snippet):
    cleaned_txt = None
    
    cleaned = re.split("<[^>]+>",str(txt_snippet)) #split to remove html tags e.g. <a>
    cleaned_txt = " ".join(s.strip() for s in cleaned if s.strip())
    return cleaned_txt
    
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

# Weibo mobile website api allows at most 100 pages of results for a keyword
for i in range(0,100): 
    url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"+keyword+"&page_type=searchall&page="+str(i)
    print('page ',i) 
    h = requests.get(url, headers=headers)
    j_obj = h.json()     
    if j_obj:
        blogposts = list()
        blogposts_raw = list()
        blog_ids = list()
        count = 0
        word_count = 0
        
        #load weibo post ids that has been extracted in the past
        done_record = 'id_extracted_'+keyword+'.txt'
        if os.path.exists(done_record):
            f = open(done_record,encoding="utf-8")
            done_entries = set(json.load(f))
            f.close()
        else:
            done_entries = None
        
        #start extraction
        #j_obj['data']['cards'] is a list of total 10 posts on a single search result page
        for post in j_obj['data']['cards']: 

            if 'mblog' in post.keys():
                blogpost = post['mblog']
                #keep a copy of the raw extractions as well
                blogposts_raw.append(blogpost)
                
                blogpost_dict = dict()
                try:
                    #extract required fields of weibo posts
                    blogpost_dict['created_at'] = get_uniform_date(blogpost['created_at'])
                    print(blogpost['created_at'])
                    print(get_uniform_date(blogpost['created_at']))
                    blogpost_dict['id'] = blogpost['mid']
                    blogpost_dict['text'] = get_cleaned_txt(blogpost['text'])
                    blogpost_dict['user'] = str(blogpost['user']) #this is a dict containing username and user description etc
                    
                    blog_ids.append(blogpost_dict['id'])
                    
                    #extracting some other fields for future reference，manual removal of duplicates and annotation needs(identify users of irrelevant blogs)
                    if 'textLength' in blogpost.keys():
                        blogpost_dict['textLength'] = blogpost['textLength']
                    else:
                        blogpost_dict['textLength'] = len(get_cleaned_txt(blogpost['text'])) 
                    
                    
                    blogpost_dict['screen_name'] = blogpost['user']['screen_name']
                    blogpost_dict['verified_type'] = blogpost['user']['verified_type']
                    blogpost_dict['user_description'] = blogpost['user']['description']        
                    if blogpost['isLongText']:
                        blogpost_dict['longText']= get_cleaned_txt(blogpost['longText']['longTextContent'])
                    
                    #record the extracted fields
                    # filter out text of less than 5 words
                    # filter out media accounts and company accounts on Weibo to gauge consumer sentiment only
                    # Only verified_types -1,0,1,200 and 220 are personal accounts.
                    if blogpost_dict['textLength'] > 5 and blogpost_dict['id'] not in done_entries and blogpost_dict['verified_type'] in [-1,0,1,200,220]: 
                        blogposts.append(blogpost_dict)
                        word_count += int(blogpost_dict['textLength']) #a count of texts on each page to keep track of extraction progress
                except:
                    print('error at',count)
                    print("Unexpected error:", sys.exc_info()[0])
                    
                    continue
            count +=1
        print(len(blogposts))
        print(word_count)
        
        #export with Pandas
        df = pd.DataFrame(blogposts)
        df = df.drop_duplicates()
        
        df.to_csv('weibo_'+keyword+'_scrap_fullstr.csv', index=False, mode='a', encoding='gb18030',header=False)
        
        #keep track of id extracted to check duplicate/ restore suspended extraction
        with open('id_extracted_'+keyword+'.txt','w',encoding = 'utf-8') as dout:
            json.dump(blog_ids,dout)
            
        #export raw json as well
        with open('done_'+keyword+'.txt','a',encoding = 'utf-8') as lout:
            json.dump(j_obj,lout)
        
        blogpost_full_df = pd.DataFrame(blogposts_raw)
        blogpost_full_df.to_csv('weibo_'+keyword+'_raw_fullstr.csv', index=True, mode='a', encoding='gb18030',header=True)
        
        
        time.sleep(30)    
    else:
        print("page",i,"returns nothing/does not exist")
        break