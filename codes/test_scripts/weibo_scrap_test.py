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

temp_cookie = 'SINAGLOBAL=5226556896257.333.1582413180515; _s_tentry=www.google.com; UOR=,,www.google.com; Apache=7762854567407.076.1582780723997; ULV=1582780724577:2:2:1:7762854567407.076.1582780723997:1582413181275'
browser_info = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

#Need to collect a list of urls that corresponds to Chinese names of the 5 big tech companies
##keyword search: #Apple/苹果
url1 = 'https://s.weibo.com/weibo?q=%23Apple%23&Refer=SWeibo_box'
url2 = 'https://s.weibo.com/weibo?q=%23%E8%8B%B9%E6%9E%9C%23&Refer=SWeibo_box'
##谷歌/Google 
url3 = 'https://s.weibo.com/weibo?q=%23%E8%B0%B7%E6%AD%8C%23&Refer=SWeibo_box'
#微软/Microsoft
url4 = 'https://s.weibo.com/weibo?q=%23%E5%BE%AE%E8%BD%AF%23&Refer=SWeibo_box'
#亚马逊/Amazon
url5 = 'https://s.weibo.com/weibo?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&Refer=SWeibo_box'
url6 = 'https://s.weibo.com/weibo?q=%23amazon%23&Refer=SWeibo_box'
#脸书/facebook
url7 = 'https://s.weibo.com/weibo?q=%23%E8%84%B8%E4%B9%A6%23&Refer=SWeibo_box'
url8 = 'https://s.weibo.com/weibo?q=%23facebook%23&Refer=SWeibo_box'

#other post ranking(integrated ranking above)-- realtime ranking; hot ranking; 
#https://s.weibo.com/realtime?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&rd=realtime&tw=realtime&Refer=weibo_realtime
#https://s.weibo.com/hot?q=%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23&xsort=hot&suball=1&tw=hotweibo&Refer=realtime_hot

#comments on officialaccounts
#https://www.weibo.com/amazonchina?is_hot=1#1583046422222


#can add lowercase and nickname e.g.Fb
keywords_list = ['Apple','%E8%8B%B9%E6%9E%9C','Google','%E8%B0%B7%E6%AD%8C','%E5%BE%AE%E8%BD%AF','Microsoft','%E4%BA%9A%E9%A9%AC%E9%80%8A','Amazon','%E8%84%B8%E4%B9%A6','Facebook']
#keywords_list = ['%23Apple%23','%23%E8%8B%B9%E6%9E%9C%23','%23Google%23','%23%E8%B0%B7%E6%AD%8C%23','%23%E5%BE%AE%E8%BD%AF%23','%23Microsoft%23','%23%E4%BA%9A%E9%A9%AC%E9%80%8A%23','%23Amazon%23','%23%E8%84%B8%E4%B9%A6%23','%23Facebook%23']
keywords_cat = ['Apple','Apple','Google','Google','Microsoft','Microsoft','Amazon','Amazon', 'Facebook','Facebook']

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
# =============================================================================
# verified_type的字段：. -1普通用户;. 0名人,. 1政府,. 2企业,. 3媒体,. 4校园,. 5网站,. 6应用,\
#. 7团体（机构）,. 8待审企业,. 200初级达人,. 220中高级达人
# --exclude non-person:1,2,3,4,5,6,7,8
# -- remaining -1, 0, 200, 220
# =============================================================================
    

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
    
    #each of the 20 entries contains a <div> block of feed_list_content and a <p> block for the creation_time
    from_snippets = soup.find_all("p","from")
    txt_snippets = soup.find_all(attrs={"node-type": "feed_list_content"})
    
    weibo_page_posts = []
    count = 0
    word_count = 0
    done_posts = set()
    weibo_post_backups =[]
    
    for pair in zip(txt_snippets, from_snippets):
        #print(count)
        weibo_post_info = dict()
        #save a copy of the txt_snippet and from_snippet for later reference
        
        weibo_post_backup = dict()
        weibo_post_backup['count'] = count
        weibo_post_backup['rawtxt'] = pair[0]
        weibo_post_backup['rawfrom'] = pair[1]
        weibo_post_backups.append(weibo_post_backup)
        
        
        try:
            #get weibo user info
            
            #get weibo user name
            
            username = re.findall('<p[^>]+nick-name="(.+)" node-type="feed_list_content_full">',str(pair[0]))[0]
            weibo_post_info['username'] = username
            
            #extract weibo post that is bounded by <p>..</p>
            content_with_tags = re.findall('<p[^>]+>(.+)</p>',str(pair[0]),flags=re.DOTALL)[0]
            #cleanup html tags
            content_split = re.split("</.>",content_with_tags)
            content_cleaned = []
            for s in content_split:
                #need to remove extra things at the end of paragraph. 
                #remove "展开全文" means "unfold this truncated text to full text"
                
                content_cleaned.append(re.sub("<[^>]+>","",s).replace("收起全文","").strip())
            cleaned_entry = " ".join(content_cleaned)
            weibo_post_info['content'] = cleaned_entry.strip()
            word_count += len(weibo_post_info['content'])
            
            #extract creation time
            #two formats of creation time: (今天 means today)今天22:19|2月3日 22:19
            if re.findall("今天\d{2}:\d{2}",str(pair[1])):
                d = datetime.datetime.today()
                today_format = str(d.year)+"-"+str(d.month)+"-"+str(d.day)+" "
                #print(re.findall("今天\d{2}:\d{2}",str(pair[1]))[0])
                datetime = re.findall("今天\d{2}:\d{2}",str(pair[1]))[0].replace("今天",today_format)
            elif re.findall("((\d{2}).(\d{2}). *(\d{2}):(\d{2}))",str(pair[1])):
                date_ch, month,day,minute,second = re.findall("((\d{2}).(\d{2}). *(\d{2}):(\d{2}))",str(pair[1]))[0]
                t_obj = time.strptime(date_ch, "%m月%d日 %M:%S")
                datetime = time.strftime("%Y-%m-%d %M:%S",t_obj).replace('1900','2020')
            weibo_post_info['created_at'] = datetime
            
            #add to done_posts to avoid future repulication by unique key(same_user,same_time)
            done_posts.add(username+datetime)
        except:
            continue
    
        #print(weibo_post_info)
        weibo_page_posts.append(weibo_post_info)
        count += 1
        
    print(len(weibo_page_posts)) # about 20 entries extracted
    print("word counts for one search results page for"+keyword+":",word_count)
    

    
    
    ##export to a csv file
    
    #identify lang: zh-cn, zh-tw by weibo site: weibocn, weibotw
    #use encoding = 'GB18030' to read in excel
    
    #check if the entry has been processed last time by loading historic keys
    done_record = 'done_posts_'+keywords_cat[i]+'.txt'
    if os.path.exists(done_record):
        f = open(done_record,encoding="utf-8")
        done_entries = set(json.load(f))
        f.close()
    else:
        done_entries = None
    
    
    with open('weibo_'+keywords_cat[i]+'_scrap_string_excelread.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username','created_at','content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        #writer.writeheader() #only write for the first time
        for weibo_post_info in weibo_page_posts:
            if done_entries:
                if weibo_post_info['username']+weibo_post_info['created_at'] not in done_entries:
                    writer.writerow(weibo_post_info)
            else:
                writer.writerow(weibo_post_info)
    

    #export done_posts to a file -- cannot use 'a' mode, otherwise not only one list but many lists
    with open('done_posts_'+keywords_cat[i]+'.txt','w',encoding = 'utf-8') as dout:
        ## json dump will turn everyitem into a list
        #done_posts.update(done_entries)
        json.dump(list(done_posts),dout)
        
    #export weibo_post_backup
    with open('weibo_'+keywords_cat[i]+'_backup.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['count','rawtext','rawfrom']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for weibo_post_backup in weibo_post_backups:
            writer.writerow(weibo_post_backup)
    
    #rest before going onto next keyword search results
    time.sleep(30)
