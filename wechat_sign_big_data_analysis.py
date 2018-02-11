#!/usr/bin/env python
# coding:utf8

import itchat
import os
import plotlib
import numpy as np
import pandas as pd
import win32com.client
import requests
from bs4 import BeautifulSoup
import json
from requests.auth import HTTPBasicAuth
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image
import re

# 扫二维码登录
itchat.auto_login(hotReload=False)

from itchat.content import *
global count
global freiends
count = 1
def webinfo(count):
    url = 'http://www.dapenti.com/blog/index.asp'
    res = requests.get(url)
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text,'html.parser')
    penti = u"喷嚏网\n"
    for news in soup.select('li'):
        title = news.select('a')[0].text
        href =  'http://www.dapenti.com/blog/'+news.select('a')[0]['href']
        count -= 1
        if count <= 0:
            penti = penti + title + href +"\n"
            break
    return penti

def get_count(Sex):
    counts = {} #初始化一个字典
    for x in Sex:
        try:
            counts[x] += 1
        except:
            pass
    return counts
    
def friendsstatic():
    global friends
    friends = itchat.get_friends(update=True)
    NickName = friends[0].NickName #获取自己的昵称
    number_of_friends = len(friends)
    df_friends = pd.DataFrame(friends)
    Sex = df_friends.Sex
    Sex_count = get_count(Sex)
    Sex_count = Sex.value_counts() #defaultdict(int, {0: 31, 1: 292, 2: 245}
    Province = df_friends.Province
    Province_count = Province.value_counts()
    Province_count = Province_count[Province_count.index!=''] #有一些好友地理信息为空，过滤掉这一部分人。
    City = df_friends.City #[(df_friends.Province=='北京') | (df_friends.Province=='四川')]
    City_count = City.value_counts()
    City_count = City_count[City_count.index!='']
    Signatures = df_friends.Signature
    regex1 = re.compile('<span.*?</span>') #匹配表情
    regex2 = re.compile('\s{2,}')#匹配两个以上占位符。
    Signatures = [regex2.sub(' ',regex1.sub('',signature,re.S)) for signature in Signatures] #用一个空格替换表情和多个空格。
    Signatures = [signature for signature in Signatures if len(signature)>0] #去除空字符串
    text = ' '.join(Signatures)
    wordlist = jieba.cut(text, cut_all=True)
    word_space_split = ' '.join(wordlist)
    coloring = np.array(Image.open("123.jpg")) #词云的背景和颜色。这张图片在本地。
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
    mask=coloring, max_font_size=60, random_state=42, scale=2,
    font_path="C:\Windows\Fonts\msyhl.ttc").generate(word_space_split) #生成词云。font_path="C:\Windows\Fonts\msyhl.ttc"指定字体，有些字不能解析中文，这种情况下会出现乱码。
    file_name_p = 'out.jpg'
    my_wordcloud.to_file(file_name_p)
    
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def getmsg(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者
    global count
    if msg['Text'] == 'n':
        count += 1
        reply = webinfo(count)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复‘n’！上一条请回复‘p’',msg['FromUserName'])
        return count

    elif msg['Text'] == 'p':
        count -= 1
        reply = webinfo(count)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复‘n’！上一条请回复‘p’',msg['FromUserName'])  
        return count
    elif msg['Text'] == 'a':
        friendsstatic()
        itchat.send_image('out.jpg',msg['FromUserName'])
    else:
        itchat.send(u'嗨！我是机器人，主人不在，我将为你提供最新的喷嚏网信息！',msg['FromUserName'])
        reply = webinfo(1)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复‘n’！上一条请回复‘p’',msg['FromUserName']) 

itchat.run()
