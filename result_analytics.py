#coding:utf-8
'''
提取百度排名的原始数据，计算首页排名词数，首页展现量，排名质量分，竞争对手等
'''

import csv,re

def search(req,line):
    text = re.search(req,line)
    if text:
        data = text.group(1)
    else:
        data = 'no'
    return data

csvfile = file('serp_html.csv','rb')
reader = csv.reader(csvfile)

'''输出百度搜索结果数据：当前关键词，排名，排名网站，百度url（需转义后才是真实的url），标题'''
for line in reader:
	word = line[0]
	html = line[1]

	number = search(r'id="(\d+)"',html)
	domain = search(r'<span class="g">(.*?)/.*</span>',html)
	bdurl = search(r'href="(http://www.baidu.com/link\?url=[^"]*?)"',html)
	title = search(r'"title":"([^"]*?)"',html)

	print '%s,%s,%s,%s,%s' % (word,number,domain,bdurl,title)




# kz = 0
# jb = 0
# zz = 0
# j5 = 0
# wb = 0
# wl = 0
# gj = 0

# csvfile = file('rank_detail.csv','rb')
# reader = csv.reader(csvfile)
# for line in reader:
# 	word = line[0]
# 	kanzhun = line[1]
# 	zhaopin = line[2]
# 	wealink = line[3]
# 	jobui = line[4]
# 	job51 = line[5]
# 	wuba = line[6]
# 	ganji = line[7]

# 	if kanzhun != '0':kz += 1
# 	if zhaopin != '0':zz += 1
# 	if wealink != '0':wb += 1
# 	if jobui != '0':jb += 1
# 	if job51 != '0':j5 += 1
# 	if ganji != '0':gj += 1
# 	if wuba != '0':wb += 1

# print '排名首页数量，看准:%s，智联:%s，若邻:%s，职友集:%s，51job:%s，赶集:%s，五八:%s' % (str(kz),str(zz),str(wb),str(jb),str(j5),str(gj),str(wb))