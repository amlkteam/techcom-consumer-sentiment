# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 22:01:53 2020

@author: gen80

weibo web-scrapping trial

reference tutorial(in Chinese): https://blog.csdn.net/Caarolin/article/details/80379967

"""
import requests
from bs4 import BeautifulSoup
import re
import csv

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

#now create a simulated browser object
headers = {'Cookies':temp_cookie,
           'User-Agent': browser_info}

#only trying out the 'Apple' keyword in this proof-of-concept
#every keyword should store into a separate csv file

#this returns one-page-only search results of about 20 entries 
h = requests.get(url1, headers=headers)
#print(h.text)

soup = BeautifulSoup(h.text,"lxml")

#each of the 20 entries contains a <div> block of feed_list_content and a <p> block for the creation_time
from_snippets = soup.find_all("p","from")
txt_snippets = soup.find_all(attrs={"node-type": "feed_list_content"})

weibo_page_posts = []
count = 0
for pair in zip(txt_snippets, from_snippets):
    #print(count)
    weibo_post_info = dict()
    try:
        #get weibo user name
        weibo_post_info['username'] = re.findall('<p[^>]+nick-name="(.+)" node-type="feed_list_content">',str(pair[0]))[0]
        
        #extract weibo post that is bounded by <p>..</p>
        content_with_tags = re.findall('<p[^>]+>(.+)</p>',str(pair[0]),flags=re.DOTALL)[0]
        #cleanup html tags
        content_split = re.split("</.>",content_with_tags)
        content_cleaned = []
        for s in content_split:
            content_cleaned.append(re.sub("<[^>]+>","",s).replace("展开全文","").replace(" c","").strip())
        cleaned_entry = " ".join(content_cleaned)
        weibo_post_info['content'] = cleaned_entry.strip() 
        
        #extract creation time
        #two formats of creation time: 今天22:19|2月3日 22:19
        weibo_post_info['datetime'] = re.findall("(?:今天|\d{2}.\d{2}.) *\d{2}:\d{2}",str(pair[1]))[0]
    except:
        continue

    #print(weibo_post_info)
    weibo_page_posts.append(weibo_post_info)
    count += 1
    
print(len(weibo_page_posts)) # about 20 entries extracted

##export to a csv file
with open('weibo_apple_scrap_string.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['username', 'content','datetime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #writer.writeheader() #only write for the first time
    for weibo_post_info in weibo_page_posts:
        writer.writerow(weibo_post_info)
