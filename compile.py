#coding=gbk

import svn
import svn.remote
import os
import shutil
import fnmatch

ret=''
workpath='\\svn temp1'
sourcedir='file:///f:/net/'

def exportfile():
    try:
        r=svn.remote.RemoteClient(sourcedir+'trunk','swift','123')
        if os.path.exists(os.getcwd()+workpath)==True:
            shutil.rmtree(os.getcwd()+workpath)
        #r.export(os.getcwd()+workpath)
        r.checkout(os.getcwd()+workpath)
        #r.run_command('commit')
    except Exception,e:
        print e
        return e
    #shutil.rmtree(os.getcwd()+'\\svn temp')
def compile(env,tagname):
    exportfile()
    if env=='.net':
        try:
            getprojfilepath()
            print ret
            cmd='cd '+ret+'& msbuild /p:VisualStudioVersion=12.0' 
            res=os.system(cmd)
            if res==0:  
                os.chdir(workpath[1:len(workpath)])
                r=svn.remote.RemoteClient(sourcedir,'swift','123')
                path=['-m','"commit"']
                #r.run_command('revert',[])
                print r.run_command('commit',path)
                print r.copy(sourcedir+'trunk', sourcedir+'tags/'+tagname)
                return 'success'
            else:
                return 'failed'
        except Exception,e:
            print e
            return e
    if env=='java':
        os.chdir(workpath[1:len(workpath)])
        res=os.system('ant')
        if res==1:
            return 'success'
        else:
            return 'failed'
def iterfindfiles(path, fnexp):
    global ret
    for root, dirs, files in os.walk(path): 
        for filename in fnmatch.filter(files, fnexp): 
            yield os.path.join(root, filename)
            ret+=root      
def getprojfilepath():
    for filename in iterfindfiles(os.getcwd(), "*.csproj"): 
        print filename
if __name__=="__main__":
    compile('.net','fas')