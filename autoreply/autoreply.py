#!/usr/bin/env python
# coding:utf8
import itchat
import os
import plotlib
import pandas as pd
import win32com.client
import requests
from bs4 import BeautifulSoup
import json
import re
from requests.auth import HTTPBasicAuth
# 扫二维码登录
itchat.auto_login(hotReload=False)

from itchat.content import *
global count
global jobFlag
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

#-*- coding:utf-8 -*-



def check_exsit(process_name):
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        return 1
    else:
        return 0

if __name__ == '__main__':
    check_exsit('notepad.exe')
# 处理文本类消息
# 包括文本、位置、名片、通知、分享
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def getmsg(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者
    global count
    if msg['Text'] == '1':
        itchat.send(u'请输入你名字：',msg['FromUserName'])
    elif msg['Text'] == '2':
        itchat.send(u'请输入你的名字：',msg['FromUserName'])
    elif msg['Text'] == '3':
        itchat.send(u'留个言就行了！',msg['FromUserName'])
    elif msg['Text'] == '4':
        reply = webinfo(1)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复41！上一条请回复42',msg['FromUserName'])

    elif msg['Text'] == '41':
        count += 1
        reply = webinfo(count)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复41！上一条请回复42',msg['FromUserName'])
        return count

    elif msg['Text'] == '42':
        count -= 1
        reply = webinfo(count)
        itchat.send(reply,msg['FromUserName'])
        itchat.send(u'下一条请回复41！上一条请回复42',msg['FromUserName'])
        return count

    elif msg['Text'] == u'王予津':
        itchat.send(u'我爱你!!!!',msg['FromUserName'])
    elif msg['Text'] == u'王予津':
        itchat.send(u'有本事你和机器人聊天到天亮',msg['FromUserName'])
    elif msg['Text'] == u'王予津':
        itchat.send(u'我爱你!!!!妈妈！',msg['FromUserName'])



    else:    
        itchat.send(u'主人已经睡觉了！现在是机器人自动回复\n 请选择你和我的关系：\n 1. 父母\n 2.女朋友\n 3.同学or同事\n 4.喷嚏网',msg['FromUserName'])
 
itchat.run()