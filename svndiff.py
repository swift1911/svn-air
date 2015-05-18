import svn
import subprocess
import os
import sshupload

def showdiff(path1,path2):
    cmd='svn diff --summarize --new %s --old %s'%('"'+path1+'"',path2)
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    filestr=p.stdout.read()
    filestr=filestr.replace('M','').replace(' ','')
    print filestr
    files=[]
    files=filestr.split('\r\n')
    print files
    return files    
if __name__=="__main__":
    showdiff('https://192.168.10.110/svn/svn-air-test/trunk','c:\\svn-air-test\\trunk')
    
