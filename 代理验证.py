#coding:utf-8
#! /usr/bin/env python
# 验证代理ip可用性，将可用的ip保存到‘daili.txt’

import urllib2,zlib,json
import re
import sys
import chardet
import threading
import time
import urllib,os

rawProxyList = []
checkedProxyList = []

print "开始获取http代理>>>>>>>>>>>>>>>>>>"

#正则提取模块
def search(req,line):
    text = re.search(req,line)
    if text:
        data = text.group(1)
    else:
        data = 'no'
    return data

#<!-- 代理来源：购买三方代理api接口，或引入采集代理py，定时循环 -->
#<!-- 获取代理ip保存至本地，格式为192.168.0.01:8088 -->

dailitxt = open('alldaili.txt','w')
url1 = 'http://proxy.goubanjia.com/api/get.shtml?order=1074074734482818&num=150&carrier=0&protocol=0&sp1=1&sort=1&system=1&rettype=1&seprator=%0D%0A'
#峰哥提供的IP
url2 = 'http://192.168.1.251:9099/api/proxies'
url3 = 'http://api.kxdaili.com/?api=20150707200040011100200028083585&dengji=%E9%AB%98%E5%8C%BF&checktime=10%E5%88%86%E9%92%9F%E5%86%85&gb=2'
url4 = 'http://proxy.mimvp.com/api/fetch.php?orderid=860150817140955617&num=150&http_type=1&anonymous=5'


#解决经过gzip压缩的网页乱码的问题
request = urllib2.Request(url1)
request.add_header('Accept-encoding', 'gzip')
opener = urllib2.build_opener()
response = opener.open(request)
html = response.read()
gzipped = response.headers.get('Content-Encoding')
if gzipped:
    html = zlib.decompress(html, 16+zlib.MAX_WBITS)
dailitxt.write(html)


#解决经过gzip压缩的网页乱码的问题
request = urllib2.Request(url3)
request.add_header('Accept-encoding', 'gzip')
opener = urllib2.build_opener()
response = opener.open(request)
html = response.read()
gzipped = response.headers.get('Content-Encoding')
if gzipped:
    html = zlib.decompress(html, 16+zlib.MAX_WBITS)
dailitxt.write(html)


request = urllib2.Request(url4)
request.add_header('Accept-encoding', 'gzip')
opener = urllib2.build_opener()
response = opener.open(request)
html = response.read()
gzipped = response.headers.get('Content-Encoding')
if gzipped:
    html = zlib.decompress(html, 16+zlib.MAX_WBITS)
dailitxt.write(html)

dailitxt.close()


#<!-- 读取代理ip文件，以list形式赋值给rawProxtList -->
for ip in open('alldaili.txt'):
    ip = ip.strip()
    rawProxyList.append(ip)
    number = len(rawProxyList)
print "以获取%s个代理" % number
        
#<!-- 验证代理的类 -->
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 10
        self.testUrl = "http://www.baidu.com/"
        #self.testStr = "030173"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s' % proxy})
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]
            t1 = time.time()
            
            try:
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                #pos = result.find(self.testStr)
                
                title = re.search(r'<title>(.*?)</title>',urllib2.urlopen('http://www.baidu.com').read())
                if title:
                    haosou_title = title.group(1)
                else:
                    haosou_title = '无法打开网页'

                print "IP:%s,链接速度:%s,title:%s" % (proxy,timeused,haosou_title)

                if (timeused < 5) and haosou_title == '百度一下，你就知道':
                    checkedProxyList.append((proxy,timeused))
                else:
                    continue
                

            except Exception,e:
                print e.message
                continue
                       
    def sort(self):
        sorted(checkedProxyList,cmp=lambda x,y:cmp(x[1],y[1]))
                 
    def run(self):
        self.checkProxy()
        self.sort()

print "开始验证http代理>>>>>>>>>>>>>>>>>>>>>>>"                
if __name__ == "__main__":
    getThreads = []
    checkThreads = []
    
    #开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(35):
        t = ProxyCheck(rawProxyList[((len(rawProxyList)+34)/35) * i:((len(rawProxyList)+34)/35) * (i+1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()


    for i in range(len(checkThreads)):
        checkThreads[i].join()

    print "\n"
    print ".......................总共%s个代理，共有%s个通过校验......................." % (len(rawProxyList),len(checkedProxyList))

    #合格ip添加至本地文件，再次写入时先清空在写入，防止ip重复
    f= open("hege_daili.txt",'w+')
    for proxy in checkedProxyList:
        print "qualified: %s\t%s" % (proxy[0],proxy[1])
        f.write(proxy[0]+"\n")
    f.close()

