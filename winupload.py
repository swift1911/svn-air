import os
def winup(hostpath,files,projname,tagname):
    for f in files:
        print f
        dirpath=os.path.dirname(f)
        dirpath=dirpath[3:len(dirpath)]
        p='\\'+'%s\\%s\\%s\\%s'%(hostpath,projname,tagname,dirpath)
        if os.path.exists(p)==False:
            mkcmd='mkdir -p '+p
            os.system(mkcmd)
        os.system('copy '+f+' %s /y'%(p))
        