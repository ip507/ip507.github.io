# -*- coding:utf-8 -*-

import urllib
import datetime
import shutil
import os
import smtplib  
from email.mime.text import MIMEText

mailto_list=["autoipsend@126.com"] 
mail_host="smtp.126.com"  #url of stmp server
mail_user="autoipsend@126.com"    #user id
mail_pass="357pis"   #user password
mail_postfix="126.com"  #url of stmp

#send email
def send_mail(to_list,sub,content):  
    me="IP Auto Sender"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
	
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
	
	#dns
	fipdns = open('LastIPDNS.txt')
	lastipdns = fipdns.read()
	fipdns.close()
	
	#mail
	fipmail = open('LastIPMAIL.txt')
	lastipmail = fipmail.read()
	fipmail.close()
	
	#get current ip
	strIP = GetIP()
	
	#send email
	if strIP != lastipmail:
		if send_mail(mailto_list,"Lastest IP",strIP):
			fip = open('LastIPMAIL.txt','w')
			fip.write(strIP)
			fip.close()
		
	#decide if refresh blog (and send mail)
	if strIP != lastip:	
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
			
	#decide if refresh ddns
	if strIP != lastipdns:
		returnCode = urllib.urlopen('http://autoipsend:357pis@ddns.oray.com/ph/update?hostname=ip507.wicp.net&myip=' + strIP + '&mode=http&user=autoipsend&password=357pis').getcode()
		if returnCode == 200:
			fip = open('LastIPDNS.txt','w')
			fip.write(strIP)
			fip.close()
