import subprocess
import os
def winup(hostpath,files,projname):
    for f in files:
        print f
        dirpath=os.path.dirname(f)
        dirpath=dirpath[3:len(dirpath)]
        if os.path.exists('%s\\%s\\%s'%(hostpath,projname,dirpath))==False:
            mkcmd='mkdir -p %s\\%s\\%s'%(hostpath,projname,dirpath)
            subprocess.Popen(mkcmd)
        subprocess.Popen('copy '+f+' %s\\%s\\%s /y'%(hostpath,projname,dirpath))