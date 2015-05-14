import smtplib  
from email.mime.text import MIMEText  
from mongodbaction import mongodbaction
mailto_list=[] 
mail_host="smtp.exmail.qq.com"  
mail_user="duyalin@aidaijia.com"   
mail_pass="mln2009"
mail_postfix="XXX.com"
  
def send_mail(to_list,sub,content):  
    me="svn air"+"<"+mail_user+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:
        server = smtplib.SMTP()
        #server.set_debuglevel(1)
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        
        server.sendmail(me, to_list, msg.as_string())
        
        server.close()
        return True
    except Exception, e:  
        print str(e)  
        return False
    
def sendtogroup(group,theme,msg):
    global mailto_list
    mailto_list=[]
    db=mongodbaction()
    cursor=db.authtogetmailaddress(group)
    if cursor!=None:
        for c in cursor:
            mailto_list.append(c.get('usermail'))
        send_mail(mailto_list,theme,msg)
if __name__ == '__main__':
    db=mongodbaction()
    cursor=db.authtogetmailaddress('develop')
    if cursor!=None:
        for c in cursor:
            mailto_list.append(c.get('usermail'))
        if send_mail(mailto_list,"hello","hello world"):  
            print "success"  
        else:  
            print "fail" 