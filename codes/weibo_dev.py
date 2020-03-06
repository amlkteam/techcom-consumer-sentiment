# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 13:37:00 2020

@author: gen80

testing on weibo developer api access

testing on scraping weibo comment
code tutorial from: https://blog.csdn.net/Caarolin/article/details/80379967

————————————————
版权声明：本文为CSDN博主「Caarolin」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Caarolin/article/details/80379967
"""

##seems only certain api are available for ordinary developer access
# =============================================================================
# https://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI#.E5.BE.AE.E5.8D.9A
# 微博
# 读取接口	statuses/home_timeline	获取当前登录用户及其所关注用户的最新微博
# statuses/user_timeline	获取用户发布的微博
# statuses/repost_timeline	返回一条原创微博的最新转发微博
# statuses/mentions	获取@当前用户的最新微博
# statuses/show	根据ID获取单条微博信息
# statuses/count	批量获取指定微博的转发数评论数
# statuses/go	根据ID跳转到单条微博页
# emotions	获取官方表情
# 写入接口	statuses/share	第三方分享链接到微博 
# =============================================================================


# this works -- statuses/home_timeline
# https://api.weibo.com/2/statuses/home_timeline.json?access_token=2.00b_cFvCu3s3cE6dd3a12f7825MvoB
import requests
import json
import re
import pandas as pd
import time
import datetime
import sys
import urllib

# ======this returns a very readily use dictionary!=======================================================================
keyword = "Apple"
#url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3Dipad&page_type=searchall&page=2'

# url = 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3DApple'
# 苹果
# https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E8%8B%B9%E6%9E%9C
# #苹果#
# https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%23%E8%8B%B9%E6%9E%9C%23

## this does the encode transformation
#urllib.parse.quote_plus('苹果')
#Out[46]: '%E8%8B%B9%E6%9E%9C'

# url = 'https://m.weibo.cn/api/comments/show?id=4073157046629802&page=1'
#keyword = urllib.parse.quote_plus('亚马逊')
# Apple 1st 20p done
# Microsoft only 3p then error
# Facebook 50 p done on Mar2
# Google 63 p done on Mar2 2:25pm -- 591 entries
# Microsoft 41 p done on Mar2 19:34pm --376 entries
# #苹果# 60p done on Mar2 21:05pm --552 entries
# '谷歌' 100p done on Mar2 10:26pm 
# '脸书' 100p done on Mar2 11:46pm
# '微軟' 94p done on Mar4 9:58pm
# Amazon 99p done Mar4 midnight
# '亚马逊' 99p done Mar5 11:04
# google -- Mar5 99p 11:32am

### can use product name of Google// twitter of tw/hk Chinese

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
    ## formats altogeher 16分钟前|4小时前| 刚刚 |昨天 04:17| 2月3日 | 02-19 | 2019-11-05
    if re.findall("(\d{1,2})分钟前",from_str):
        t = datetime.datetime.now()
        min_dif = int(re.findall("(\d{1,2})分钟前",from_str)[0])
        time_obj = t - datetime.timedelta(minutes=min_dif)
        created_at = time_obj.strftime("%Y-%m-%d %H:%M:%S")
    elif re.findall("(\d{1,2})小时前",from_str):
        t = datetime.datetime.now()
        min_dif = int(re.findall("(\d{1,2})小时前",from_str)[0])
        time_obj = t - datetime.timedelta(hours=min_dif)
        created_at = time_obj.strftime("%Y-%m-%d %H:%M:%S")    
    elif re.findall("刚刚",from_str):
        t = datetime.datetime.now()
        created_at = t.strftime("%Y-%m-%d %H:%M:%S")
    elif re.findall("(昨天 (\d{2}):(\d{2}))",from_str):
        d = datetime.datetime.now()
        date_ch,h,m = re.findall("(昨天 (\d{2}):(\d{2}))",from_str)[0]
        date_obj = d - datetime.timedelta(days=1)
        combined_dt = date_obj.replace(hour = int(h), minute = int(m))
        created_at = combined_dt.strftime("%Y-%m-%d %H:%M:%S")
    elif re.findall("(\d{4})-(\d{2})-(\d{2})",from_str): 
        d = datetime.datetime.now()
        year, month, day =re.findall("(\d{4})-(\d{2})-(\d{2})",from_str)[0]
        combined_dt =d.replace(year = int(year), month=int(month),day=int(day))
        created_at = combined_dt.strftime("%Y-%m-%d %H:%M:%S")        
    elif re.findall("(\d{2})-(\d{2})",from_str): 
        d = datetime.datetime.now()
        month, day =re.findall("(\d{2})-(\d{2})",from_str)[0]
        combined_dt =d.replace(month=int(month),day=int(day))
        created_at = combined_dt.strftime("%Y-%m-%d %H:%M:%S")
        
    
    elif re.findall("((\d+)月(\d+)日)",from_str):
        date_ch, month,day = re.findall("((\d+)月(\d+)日)",from_str)[0]
        t_obj = time.strptime(date_ch, "%m月%d日")
        created_at = time.strftime("%Y-%m-%d %M:%S",t_obj).replace('1900','2020')
    else:
        created_at = None
    return created_at

for i in range(0,100): #what if less than 50?
    url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"+keyword+"&page_type=searchall&page="+str(i)
    print('page ',i) 
    h = requests.get(url, headers=headers)
    j_obj = h.json()     
    if j_obj:
        blogposts = list()
        blogposts_raw = list()
        count = 0
        word_count = 0
        for post in j_obj['data']['cards']: #j_obj['data']['cards'] is a list of 10 posts
            #print(count)
            #print(post.keys())
            if 'mblog' in post.keys():
                blogpost = post['mblog']
                blogposts_raw.append(blogpost)
                
                blogpost_dict = dict()
                try:
                    blogpost_dict['created_at'] = get_uniform_date(blogpost['created_at'])
                    print(blogpost['created_at'])
                    print(get_uniform_date(blogpost['created_at']))
                    blogpost_dict['id'] = blogpost['mid']
                    blogpost_dict['text'] = get_cleaned_txt(blogpost['text'])
                    if 'textLength' in blogpost.keys():
                        blogpost_dict['textLength'] = blogpost['textLength']
                    else:
                        blogpost_dict['textLength'] = len(get_cleaned_txt(blogpost['text']))
                    #blogpost['retweeted_status']
                    #blogpost_dict['source'] = blogpost['source']    
                    blogpost_dict['user'] = str(blogpost['user'])
                    blogpost_dict['verified'] = blogpost['user']['verified']
                    blogpost_dict['screen_name'] = blogpost['user']['screen_name']
                    blogpost_dict['verified_type'] = blogpost['user']['verified_type']
                    blogpost_dict['user_description'] = blogpost['user']['description']        
                    if blogpost['isLongText']:
                        blogpost_dict['longText']= get_cleaned_txt(blogpost['longText']['longTextContent'])
                        
                    blogpost_dict['bid'] = blogpost['bid'] 
                    blogposts.append(blogpost_dict)
                    word_count += int(blogpost_dict['textLength'])
                except:
                    print('error at',count)
                    print("Unexpected error:", sys.exc_info()[0])
                    #pass
                    continue
            count +=1
        print(len(blogposts))
        print(word_count)
        
        df = pd.DataFrame(blogposts)
        df = df.drop_duplicates()
        
        df.to_csv('weibo_'+keyword+'_scrap_fullstr.csv', index=True, mode='a', encoding='gb18030',header=False)
        
        #export source json as well
        with open('done_'+keyword+'.txt','a',encoding = 'utf-8') as dout:
            json.dump(j_obj,dout)
        
        blogpost_full_df = pd.DataFrame(blogposts_raw)
        blogpost_full_df.to_csv('weibo_'+keyword+'_raw_fullstr.csv', index=True, mode='a', encoding='gb18030',header=True)
        
        
        time.sleep(30)    
    else:
        print("page",i,"returns nothing/does not exist")
        break
# =============================================================================

# =============================================================================
# inside each dict of j:-- found in j[data] is some more dicts :
#cardlistInfo,cards,banners,scheme,showAppTips
# cards store the posts
# len(j['data']['cards']) #10

#for p in j['data']['cards']:
#    print(p.keys())
#    print("---------------")
#Out: dict_keys(['card_type', 'card_type_name', 'itemid', 'actionlog', 'display_arrow', 'show_type', 'mblog', 'scheme'])

#itemid looks like this:
#seqid:1082863721|type:1|t:|pos:2-3-5|q:ipad|ext:&cate=113&mid=4477702768052442&qri=0&qtime=1583120059&
#scheme looks like this:
# https://m.weibo.cn/status/IwISjw4li?mblogid=IwISjw4li&luicode=10000011&lfid=100103type%3D1%26q%3Dipad

#keys in mblog:
# dict_keys(['visible', 'created_at', 'id', 'idstr', 'mid', 'can_edit', 'show_additional_indication', \
#'text', 'textLength', 'source', 'favorited', 'pic_types', 'is_paid', 'mblog_vip_type', 'user', 'reposts_count', \
# 'comments_count', 'attitudes_count', 'pending_approval_count', 'isLongText', 'reward_exhibition_type', 'hide_flag', \
# 'mlevel', 'mblogtype', 'rid', 'more_info_type', 'extern_safe', 'number_display_strategy', 'content_auth', 'pic_num', \
#'status', 'digit_attr', 'dispatch_ctrl', 'kwfilter_pass', 'itemid', 'analysis_extra', 'weibo_position', 'show_attitude_bar',\
#  'obj_ext', 'page_info', 'bid'])

#to extract-- id/mid/author_mid;created_at; text; textLength; source; user(dict; verified; verified_type); isLongText ;(longText); author_name; bid

# example of one dict: 
# 
#        {'id': 4323294473822298,
#     'created_at': '2018-12-31',
#     'source': '',
#     'user': {'id': 3418003314,
#      'screen_name': 'Cressida彦伶5O',
#      'profile_image_url': 'https://tvax2.sinaimg.cn/crop.0.0.664.664.180/cbba9772ly8fgly55wgn2j20ig0igdhp.jpg?KID=imgbed,tva&Expires=1583130118&ssig=eKcn2VMB3K',
#      'verified': False,
#      'verified_type': -1,
#      'followers_count': 388,
#      'mbtype': 0,
#      'profile_url': 'https://m.weibo.cn/u/3418003314?uid=3418003314',
#      'remark': '',
#      'following': False,
#      'follow_me': False},
#     'text': "回复<a href='https://m.weibo.cn/n/长不大的鸵鸟'>@长不大的鸵鸟</a>:历史说一下就不怀好意什么逻辑？？日本人说你年年提南京大屠杀其目的肯定也是不怀好意你接受吗？？？",
#     'reply_id': 4073574857886468,
#     'reply_text': "回复<a href='https://m.weibo.cn/n/琥珀核桃双皮奶qvq'>@琥珀核桃双皮奶qvq</a>:不能拿历史说事，毕竟现在国情不同了    不知道是谁煽动这个话题的，其目的肯定是不怀好意！",
#     'like_counts': 0,
#     'liked': False}],
#   'total_number': 3772,
#   'max': 378}}
#     
# =============================================================================

#headers = {'Cookies':'Your cookie',
#            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}


# =============================================================================
# # -*- coding:utf-8 -*-
#  
# import requests
# import re
# import time
# import pandas as pd
#  
# # 把id替换成你想爬的地址id
# urls = 'https://m.weibo.cn/api/comments/show?id=4073157046629802&page={}'
#  
# headers = {'Cookies':'Your cookies',
#           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
#  
# # 找到html标签
# tags = re.compile('</?\w+[^>]*>')
#  
# # 设置提取评论function
# def get_comment(url):
#     j = requests.get(url, headers=headers).json()
#     comment_data = j['data']['data']
#     for data in comment_data:
#         try:
#             comment = tags.sub('', data['text']) # 去掉html标签
#             reply = tags.sub('', data['reply_text'])
#             weibo_id = data['id']
#             reply_id = data['reply_id']
#  
#             comments.append(comment)
#             comments.append(reply)
#             ids.append(weibo_id)
#             ids.append(reply_id)
#  
#         except KeyError:
#             pass
#  
#  
# comments, ids = [], []
# for i in range(1, 101):
#     url = urls.format(str(i))
#     get_comment(url)
#     time.sleep(10) # 防止爬得太快被封
#  
# # 这里我用pandas写入csv文件，需要设置encoding，不然会出现乱码
# df = pd.DataFrame({'ID': ids, '评论': comments})
# df = df.drop_duplicates()
# df.to_csv('观察者网.csv', index=False, encoding='gb18030')
# 
# =============================================================================
