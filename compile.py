
import svn
import svn.remote
import os
import shutil
import fnmatch
import logging
from xml.etree import ElementTree 
import Sendmail

ret=''
workpath=''
sourcedir=''
username=''
pwd=''


def exportfile():
    global workpath
    global sourcedir
    xml_file='config.xml' 
    xml=ElementTree.ElementTree(file=xml_file).getroot()
    workpath=xml.find('temppath').text
    sourcedir=xml.find('sourcedir').text
    username=xml.find('username').text
    pwd=xml.find('passwd').text
    try:
        r=svn.remote.RemoteClient(sourcedir+'trunk',username,pwd)
        if os.path.exists(os.getcwd()+"\\"+workpath)==True:
            shutil.rmtree(os.getcwd()+"\\"+workpath,True)
        r.checkout(os.getcwd()+"\\"+workpath)
        #r.run_command('commit')
    except Exception,e:
        print e
        return e
    #shutil.rmtree(os.getcwd()+'\\svn temp')
def compile(env,tagname):
    global workpath
    exportfile()
    if env=='.net':
        try:
            getprojfilepath()
            print ret
            cmd='cd '+ret+'& msbuild /p:VisualStudioVersion=12.0' 
            res=os.system(cmd)
            print res
            if res==0:
                global sourcedir
                os.chdir(workpath)
                r=svn.remote.RemoteClient(sourcedir,username,pwd)
                #print sourcedir
                path=['-m','"commit"']
                #r.run_command('revert',[])
                r.run_command('commit',path)
                path=['trunk','tags/'+tagname]
                r.copy('trunk', 'tags/'+tagname)
                os.chdir('..')
                shutil.rmtree(workpath, True)
                Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled,please test..'+'path : '+sourcedir+"/tags/"+tagname.encode())
                return 'success'
            else:
                shutil.rmtree(workpath, True)
                return 'failed'
        except Exception,e:
            shutil.rmtree(workpath, True)
            print e
            return e
    if env=='java':
        os.chdir(workpath)
        res=os.system('ant')
        if res==1:
            shutil.rmtree(workpath, True)
            return 'success'
        else:
            shutil.rmtree(workpath, True)
            return 'failed'
def iterfindfiles(path, fnexp):
    global ret
    ret=''
    for root, dirs, files in os.walk(path): 
        for filename in fnmatch.filter(files, fnexp): 
            yield os.path.join(root, filename)
            ret+=root
def getprojfilepath():
    for filename in iterfindfiles(os.getcwd()+"\\"+workpath, "*.csproj"): 
        print filename
if __name__=="__main__":
    compile('.net','.net service test')
    #compile('.net','.net service test')
    #compile('.net','.net service test')