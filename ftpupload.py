from ftplib import FTP


def ftpactivity(hostip,port,username,userpwd):
    ftpclient=FTP()
    ftpclient.debug(1)
    ftpclient.connect(hostip, port, -999)
    ftpclient.login(username, userpwd)
    fp=open('test.log','rb')
    ftpclient.storbinary('STOR', fp)
    
if __name__=="__main__":
    ftpactivity('202.195.112.14', 21, 'flkc4', 'flkc4')