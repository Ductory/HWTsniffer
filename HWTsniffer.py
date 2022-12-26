#HWTsniffer - Made by Dangfer
#功能：自动删除何杂在最爱春雷吧的帖子和回帖, 何杂爬爬爬
#第一次使用请填好你的BDUSS, fid, tbs

import requests
import hashlib
import time
from urllib.parse import urlencode

def GetThread(url):
    global fid, lastThread
    tmp = 0
    response = requests.get(url).json()
    for i in response['post_list']:
        s = i['forum_id']
        if s == fid: #在目标贴吧发帖了
            t = int(i['create_time'])
            if t > lastThread: #发了新贴
                if t > tmp: #仅更新1次
                    tmp = t
                print('何杂发帖了！', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))
                DeleteThread(i['thread_id'])
    if tmp != 0: #发了新帖
        lastThread = tmp
    return

def GetRepost(url):
    global fid, lastRepost
    tmp = 0
    response = requests.get(url).json() #这里json中的time和id是int类型的
    for i in response['post_list']:
        s = i['forum_id']
        if s == int(fid):
            t = i['create_time']
            if t > lastRepost: #回了新帖
                if t > tmp:
                    tmp = t
                print('何杂回帖了！', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))
                DeleteRepost(str(i['post_id']), str(i['thread_id']))
    if tmp != 0: #回了新帖
        lastRepost = tmp
    return

def DeleteThread(z):
    global paramDT
    paramDT['z'] = z
    paramDT['sign'] = sign(paramDT)
    url = 'http://c.tieba.baidu.com/c/c/bawu/delthread?' + urlencode(paramDT)
    response = requests.get(url).json()
    if response['error_code'] == '0':
        print('帖子删除成功')
    else:
        print('操作失败，错误信息：', response['error_msg'])
    return

def DeleteRepost(pid, z):
    global paramDP
    paramDP['pid'] = pid
    paramDP['z'] = z
    paramDP['sign'] = sign(paramDP)
    url = 'http://c.tieba.baidu.com/c/c/bawu/delpost?' + urlencode(paramDP)
    response = requests.get(url).json()
    if response['error_code'] == '0':
        print('回帖删除成功')
    else:
        print('操作失败，错误信息：', response['error_msg'])
    return

def sign(src):
    s = ''
    if 'sign' in src: #重新签名
        del src['sign']
    #生成报文
    for k, v in src.items():
        s += k + '=' + v
    s += 'tiebaclient!!!'
    return hashlib.md5(s.encode()).hexdigest()
    

#初始化
uid = '6317885792' #何杂id
lastThread = 0
lastRepost = 0
#仅获取profile的前三个帖子, 若读取发帖会一次性读60个
paramProfile = {'_client_type': '2',
                '_client_version': '7.2.0.0',
                'uid': uid}
signProfile = sign(paramProfile)
paramProfile['sign'] = signProfile
urlProfile = 'http://c.tieba.baidu.com/c/u/user/profile?' + urlencode(paramProfile)
#获取回帖
paramRepost = {'rn': '20',
               'uid': uid}
signRepost = sign(paramRepost)
paramRepost['sign'] = signRepost
urlRepost = 'http://c.tieba.baidu.com/c/u/feed/userpost?' + urlencode(paramRepost)
#删除帖子
#！----------重要----------！
#BDUSS请打开浏览器的Cookies找到其中的BDUSS
#fid请用 http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname=吧名 获取
#tbs请用 http://tieba.baidu.com/dc/common/tbs 获取
BDUSS = '你的BDUSS'
tbs = '你的tbs'
fid = '27779526' #最爱春雷吧id
#fid = '69399' #永动机吧id, 仅测试使用

paramDT = {'BDUSS': BDUSS,
           'fid': fid,
           'tbs': tbs,
           'z': ''}
paramDP = {'BDUSS': BDUSS,
           'fid': fid,
           'pid': '',
           'tbs': tbs,
           'z': ''}

while True:
    GetThread(urlProfile)
    GetRepost(urlRepost)
    time.sleep(600) #每10分钟获取一次消息
