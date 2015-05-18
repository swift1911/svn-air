import os
import subprocess
def winup(hostpath,files,projname,tagname):
    for f in files:
        print f
        dirpath=os.path.dirname(f)
        dirpath=dirpath[3:len(dirpath)]
        p='\\'+'%s\\%s\\"%s"\\%s'%(hostpath,projname,tagname,dirpath)
        if os.path.exists(p)==False:
            mkcmd='mkdir -p '+p
            subprocess.Popen(mkcmd,shell=True)
        subprocess.Popen('copy '+f+' %s /y'%(p),shell=True)
        backuppath="c:\\backup"
        backuppath=backuppath+'\\'+projname+'\\'+'"'+tagname+'"'+'\\'+dirpath
        if os.path.exists(backuppath)==False:
            subprocess.Popen('mkdir -p '+backuppath,shell=True)
        subprocess.Popen('copy '+f+' %s /y'%(backuppath),shell=True)
        
    
        