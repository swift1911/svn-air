
import subprocess

def uploaddir(dirpath,serverip,serverpath,username,pwd):
    subprocess.Popen('pscp -pw %s -r %s %s@%s:%s'%(pwd,dirpath,username,serverip,serverpath),shell=True)
