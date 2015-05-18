
import subprocess
import os
import paramiko

def uploaddir(workpath,dirpath,serverip,serverpath,username,pwd):
    subprocess.Popen('pscp -pw %s -r %s %s@%s:%s'%(pwd,dirpath,username,serverip,serverpath),shell=True)
def uploadfile(workpath,files,serverip,serverpath,username,pwd):
    sshclient=paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    sshclient.connect('192.168.10.166', 22, username,pwd)
    for f in files:
        print f
        dirpath=os.path.dirname(f)
        linuxdir=dirpath[2:len(dirpath)].replace('\\','/')
        sshclient.exec_command('mkdir -p %s%s'%(serverpath,linuxdir))       
        subprocess.Popen('pscp -pw %s %s %s@%s:%s'%(pwd,f,username,serverip,serverpath+linuxdir),shell=True)