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
	fip = open('LastIP.txt')
	lastip = fip.read()
	fip.close()
	strIP = GetIP()
	if strIP == lastip:
		exit(0)
	
	#write blog
	shutil.rmtree('_posts',True)
	os.mkdir('_posts')
	WriteGithubMDPage(strIP)
	
	#git command
	ctime = datetime.datetime.now()
	strtime = '%d-%.2d-%.2d %.2d:%.2d:%.2d' % (ctime.year,ctime.month,ctime.day,ctime.hour,ctime.minute,ctime.second)
	s1 = os.system('git add . --all')
	s2 = os.system('git commit -m \"' + strtime + '\"')
	s3 = os.system('git push origin master')
	
	if s1==0 and s2==0 and s3==0:
		fip = open('LastIP.txt','w')
		fip.write(strIP)
		fip.close()
