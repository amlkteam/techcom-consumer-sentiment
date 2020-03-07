# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:17:24 2020

@author: gen80

#modified version of multiple keywords extract
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 22:01:53 2020

@author: amy

weibo web-scrapping trial

reference tutorials(in Chinese): 
https://blog.csdn.net/Caarolin/article/details/80379967
https://blog.csdn.net/jiange_zh/article/details/47361555

"""
import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime
import time
import json
import os
import sys

temp_cookie = 'SINAGLOBAL=5226556896257.333.1582413180515; _s_tentry=www.google.com; UOR=,,www.google.com; Apache=7762854567407.076.1582780723997; ULV=1582780724577:2:2:1:7762854567407.076.1582780723997:1582413181275'
browser_info = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

#Need to collect a list of urls that corresponds to Chinese names of the 5 big tech companies
# =============================================================================
# ##keyword search: #Apple/苹果
# url1 = 'https://s.weibo.com/weibo?q=%23Apple%23&Refer=SWeibo_box'
# url2 = 'https://s.weibo.com/weibo?q=%23%E8%8B%B9%E6%9E%9C%23&Refer=SWeibo_box'
# ##谷歌/Google 
# url3 = 'https://s.weibo.com/weibo?q=%23%E8%B0%B7%E6%AD%8C%23&Refer=SWeibo_box'
# #微软/Microsoft
# url4 = 'https://s.weibo.com/weibo?q=%23%E5%BE%AE%E8%BD%AF%23&Refer=SWeibo_box'
# #亚马逊/Amazon
# url5 = 'https://s.weibo.com/weibo?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&Refer=SWeibo_box'
# url6 = 'https://s.weibo.com/weibo?q=%23amazon%23&Refer=SWeibo_box'
# #脸书/facebook
# url7 = 'https://s.weibo.com/weibo?q=%23%E8%84%B8%E4%B9%A6%23&Refer=SWeibo_box'
# url8 = 'https://s.weibo.com/weibo?q=%23facebook%23&Refer=SWeibo_box'
# =============================================================================

#other post ranking(integrated ranking above)-- realtime ranking; hot ranking; 
#https://s.weibo.com/realtime?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&rd=realtime&tw=realtime&Refer=weibo_realtime
#https://s.weibo.com/hot?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&xsort=hot&suball=1&tw=hotweibo&Refer=realtime_hot

#comments on officialaccounts
#https://www.weibo.com/amazonchina?is_hot=1#1583046422222


#can add lowercase and nickname e.g.Fb
keywords_list = ['Apple','%E8%8B%B9%E6%9E%9C','Google','%E8%B0%B7%E6%AD%8C','%E5%BE%AE%E8%BD%AF','Microsoft','%E4%BA%9A%E9%A9%AC%E9%80%8A','Amazon','%E8%84%B8%E4%B9%A6','Facebook']
#keywords_list = ['%23Apple%23','%23%E8%8B%B9%E6%9E%9C%23','%23Google%23','%23%E8%B0%B7%E6%AD%8C%23','%23%E5%BE%AE%E8%BD%AF%23','%23Microsoft%23','%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23','%23Amazon%23','%23%E8%84%B8%E4%B9%A6%23','%23Facebook%23']
keywords_cat = ['Apple','Apple','Google','Google','Microsoft','Microsoft','Amazon','Amazon', 'Facebook','Facebook']

#keywords_list = ['%23facebook%23']
#keywords_cat = ['Facebook']

#products_list = ['iphone','Iphone','ipad','applewatch','applemusic','macbook'，'Android','安卓','Youtube','油管','Windows','Surface','Bing','Hotmail','OneNote','Edge','Office','PrimeDay','Kindle','FireTablet',,'Alexa','Instagram','Whatsapp']
#for ch_kw in products_list:
    #kw_encoded = ch_kw.decode('GBK','ignore').encode('utf-8')

#a page that can show all results??--need login
# https://s.weibo.com/weibo?q=Google&nodup=1

#verfied status
#<i class="icon-vip icon-vip-b"></i> 微博官方认证
# <i class="icon-vip icon-vip-y"> 微博会员
# "微博个人认证"><i class="icon-vip icon-vip-g">
# "微博会员"><i class="icon-vip icon-member">
# title="微博达人"><i class="icon-vip icon-daren">
    
    
def get_user_link_verification(user_snippet):
    #set default for return
    user_id = None
    nickname = None
    verified_status = None
    
    if user_snippet.find_all("a","name"):
        profile_link = user_snippet.find_all("a","name")[0].get('href') #'//weibo.com/5701225412?refer_flag=1001030103_'
    if re.findall('weibo.com/(\d+)\?refer_flag=',profile_link):
        user_id = re.findall('weibo.com/(\d+)\?refer_flag=',profile_link)[0]
    if user_snippet.find_all("a","name"):
        nickname = user_snippet.find_all("a","name")[0].get('nick-name')
    if user_snippet.find_all("i","icon-vip"):
        verified_status = user_snippet.find_all("i","icon-vip")[0].get("class")[1] #<i class="icon-vip icon-member">
    
    return user_id, nickname, verified_status

def get_cleaned_txt(txt_snippet):
    cleaned_txt = None
    
    cleaned = re.split("<[^>]+>",str(txt_snippet)) #split to remove html tags e.g. <a>
    cleaned_txt = " ".join(s.strip() for s in cleaned if s.strip())
    return cleaned_txt
    
def get_uniform_date(from_snippet):
    created_at = None
    
    from_str = str(from_snippet)
    ##3 formats altogeher 16分钟前| 今天22:19 | 2月3日 22：10
    if re.findall("(\d{2})分钟前",from_str):
        t = datetime.datetime.now()
        min_dif = int(re.findall("(\d{2})分钟前",from_str)[0])
        time_obj = t - datetime.timedelta(minutes=min_dif)
        created_at = time_obj.strftime("%Y-%m-%d %M:%S")
    
    elif re.findall("今天\d{2}:\d{2}",from_str):
        d = datetime.datetime.today()
        today_format = str(d.year)+"-"+str(d.month)+"-"+str(d.day)+" "
        #print(re.findall("今天\d{2}:\d{2}",str(pair[1]))[0])
        created_at = re.findall("今天\d{2}:\d{2}",from_str)[0].replace("今天",today_format)
    elif re.findall("((\d{2}).(\d{2}). *(\d{2}):(\d{2}))",from_str):
        date_ch, month,day,minute,second = re.findall("((\d{2}).(\d{2}). *(\d{2}):(\d{2}))",from_str)[0]
        t_obj = time.strptime(date_ch, "%m月%d日 %M:%S")
        created_at = time.strftime("%Y-%m-%d %M:%S",t_obj).replace('1900','2020')
    return created_at     

#now create a simulated browser object
headers = {'Cookies':temp_cookie,
           'User-Agent': browser_info}

#only trying out the 'Apple' keyword in this proof-of-concept
#every keyword should store into a separate csv file

for i,keyword in enumerate(keywords_list):
    url_q = "https://s.weibo.com/weibo?q="+keyword+"&Refer=SWeibo_box"
    #this returns one-page-only search results of about 20 entries 
    h = requests.get(url_q, headers=headers)
    #print(h.text)
    
    soup = BeautifulSoup(h.text,"lxml")
    
    feedlist=soup.find_all(attrs={"action-type": "feed_list_item"})

    extract_feeds = []
    
    
    for c,feed in enumerate(feedlist):
       print(c)
       extract_feed = dict()
       from_snippets = feed.find_all("p","from")
       txt_snippets = feed.find_all(attrs={"node-type": "feed_list_content"})
       txt_full = feed.find_all(attrs={"node-type": "feed_list_content_full"}) #not all posts have "feed_list_content_full"
       user_info=feed.find_all("div","info")
       extract_feed['from'] = from_snippets[0]
       if txt_full:
           extract_feed['txt'] = txt_full[0]
       elif txt_snippets:
           extract_feed['txt'] = txt_snippets[0]
       extract_feed['user'] = user_info[0]
       extract_feeds.append(extract_feed)   
    
    print(len(extract_feeds))
    
    #export this raw_extract dict
    with open('weibo_'+keywords_cat[i]+'_raw_extract.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['user','from','txt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        #writer.writeheader() #only write for the first time
        for extract_feed in extract_feeds:
            writer.writerow(extract_feed)
            
    #start extractions from raw
    count = 0
    word_count = 0
    weibo_page_posts = []
    done_posts = set()
    for extract_feed in extract_feeds:
        weibo_post_info = dict()
        
        print(count)
        try:
            user_id, nickname, verified_status = get_user_link_verification(extract_feed['user'])
            cleaned_txt = get_cleaned_txt(extract_feed['txt'])
            created_at = get_uniform_date(extract_feed['from'])
            
            weibo_post_info['user_id'] = user_id
            weibo_post_info['nickname'] = nickname
            weibo_post_info['verified_status'] = verified_status
            weibo_post_info['cleaned_txt'] = cleaned_txt.replace("收起全文 d","")
            weibo_post_info['created_at'] = created_at
            
            weibo_page_posts.append(weibo_post_info)
            done_posts.add(user_id+' '+created_at)
            word_count += len(weibo_post_info['cleaned_txt'])
        except:
            #print("error occurred",count)
            print("Unexpected error:", sys.exc_info()[0])
            continue
        count += 1
        
    print(len(weibo_page_posts))    
    print(word_count)

     #check if the entry has been processed last time by loading historic keys
    done_record = 'done_posts_'+keywords_cat[i]+'.txt'
    if os.path.exists(done_record):
        f = open(done_record,encoding="utf-8")
        done_entries = set(json.load(f))
        f.close()
    else:
        done_entries = None


    with open('weibo_'+keywords_cat[i]+'_scrap_fullstr.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['created_at','user_id','nickname','verified_status','cleaned_txt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader() #only write for the first time
        for weibo_post_info in weibo_page_posts:
            if done_entries:
                if weibo_post_info['user_id'] and weibo_post_info['created_at']:
                    if weibo_post_info['user_id']+" "+weibo_post_info['created_at'] not in done_entries:
                        writer.writerow(weibo_post_info)
            else:
                writer.writerow(weibo_post_info)
    

    #export done_posts to a file -- cannot use 'a' mode, otherwise not only one list but many lists
    with open('done_posts_'+keywords_cat[i]+'.txt','w',encoding = 'utf-8') as dout:
        ## json dump will turn everyitem into a list
        if done_entries:
            done_posts.update(done_entries)
        json.dump(list(done_posts),dout)
        
# =============================================================================
#     #export weibo_post_backup
#     with open('weibo_'+keywords_cat[i]+'_backup.csv', 'a', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['count','rawtext','rawfrom']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         for weibo_post_backup in weibo_post_backups:
#             writer.writerow(weibo_post_backup)
# =============================================================================
    
    #rest before going onto next keyword search results
    time.sleep(40)
