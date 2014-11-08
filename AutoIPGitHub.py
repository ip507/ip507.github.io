# -*- coding:utf-8 -*-

import urllib
import datetime
import shutil
import os

#get ip from router web page
def GetIP():
	strRaw = urllib.urlopen("http://admin:admin@192.168.1.1/userRpm/StatusRpm.htm").read()
	index = strRaw.find("var wanPara")
	if index == -1:
		print failed
	index = strRaw.find(',',strRaw.find(',',index+1)+1)
	index = strRaw.find('"',index+1)
	indexEnd = strRaw.find('"',index+1)
	strIP = strRaw[index+1:indexEnd]
	return strIP
	
def WriteGithubMDPage(ip):
	ctime = datetime.datetime.now()
	strtime = '%.4d-%.2d-%.2d' % (ctime.year, ctime.month, ctime.day)
	fl = open('_posts/' + strtime + '-IP.md','w')
	fl.write('---\nlayout: post\ntitle: newest ip\ncategory: IP\n---\n\n')
	fl.write('##' + ip + '\n\n')
	fl.write('[Click here to go...](http://' + ip + '/)\n')
	fl.close()

if __name__ == "__main__":
	#get and ensure ip
	
	strIP = GetIP()
	
	#write blog
	shutil.rmtree('_posts',True)
	os.mkdir('_posts')
	WriteGithubMDPage(strIP)
	
	#git command
	ctime = datetime.datetime.now()
	strtime = '%d-%.2d-%.2d %.2d:%.2d:%.2d' % (ctime.year,ctime.month,ctime.day,ctime.hour,ctime.minute,ctime.second)
	print os.system('git add . --all')
	print os.system('git commit -m \"' + strtime + '\"')
	print os.system('git push origin master')
	
