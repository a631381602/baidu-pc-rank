#coding:utf-8
'''
定时执行任务，每隔1分钟，获取最新代理并验证
'''

import os,time

while 1:
	os.system("python 代理验证.py")
	time.sleep(120)