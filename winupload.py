import os
import subprocess
def winup(islocalpath,hostpath,files,projname,tagname):
    for f in files:
        print f
        dirpath=os.path.dirname(f)
        dirpath=dirpath[3:len(dirpath)]
        if islocalpath==1:
            p='%s\\%s\\"%s"\\%s'%(hostpath,projname,tagname,dirpath)
        else:
            p='\\'+'%s\\%s\\"%s"\\%s'%(hostpath,projname,tagname,dirpath)
        if os.path.exists(p)==False:
            mkcmd='mkdir -p '+p
            subprocess.Popen(mkcmd,shell=True)
        proc=subprocess.Popen('copy '+f+' %s /y'%(p),shell=True)
        print proc.wait()
        #backuppath="c:\\backup"
        #backuppath=backuppath+'\\'+projname+'\\'+'"'+tagname+'"'+'\\'+dirpath
        #if os.path.exists(backuppath)==False:
        #    subprocess.Popen('mkdir -p '+backuppath,shell=True)
        #subprocess.Popen('copy '+f+' %s /y'%(backuppath),shell=True)
        
    
        