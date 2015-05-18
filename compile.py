
import svn
import svn.remote
import os
import shutil
import fnmatch
import logging
from xml.etree import ElementTree 
import Sendmail
import log
import jsondecode
import sys
import cmd
import sshupload
import winupload
import svndiff
ret=''
workpath=''
sourcedir=''
username=''
pwd=''
defpath=os.getcwd()



def exportfile(jsonstr):
    global workpath
    global sourcedir
    logger=log.getlogger()
    xml_file=sys.path[0]+'\\config.xml' 
    xml=ElementTree.ElementTree(file=xml_file).getroot()
    workpath=xml.find('temppath').text
    sourcedir=jsondecode.jsondecode(jsonstr,'svnurl')
    username=jsondecode.jsondecode(jsonstr,'username')
    pwd=jsondecode.jsondecode(jsonstr,'userpwd')
    try:
        r=svn.remote.RemoteClient(sourcedir+'trunk',username,pwd)
        if os.path.exists(workpath)==True:
            shutil.rmtree(workpath,True)
        r.checkout(workpath)
        #r.run_command('commit')
    except Exception,e:
        logger.info(e)
        print e
        return e
    #shutil.rmtree(os.getcwd()+'\\svn temp')
def compile(env,tagname,jsonstr):
    global workpath
    logger=log.getlogger()
    logger.info(os.getcwd())
    exportfile(jsonstr)
    logger.info(jsonstr)
    if env=='.net':
        try:
            getprojfilepath()
            print ret
            logger.info(ret)
            os.chdir(workpath)
            cmd='msbuild /p:VisualStudioVersion=12.0' 
            res=os.system(cmd)
            if res==0:
                global sourcedir              
                r=svn.remote.RemoteClient(sourcedir,username,pwd)
                #print sourcedir
                files=svndiff.showdiff( sourcedir+'/trunk',workpath)
                path=['-m','"commit"']
                #r.run_command('revert',[])
                print r.run_command('commit',path)    
                l=sourcedir.split('/')
                projname=l[len(l)-2]
                winupload.winup('\\192.168.10.62\\upload', files, projname,tagname)
                           
                path=['trunk','tags/'+tagname]
                print r.copy('trunk', 'tags/'+tagname+'_compiled')
                
                
                
                
                Sendmail.sendtogroup('testing', 'version '+tagname, 'version '+tagname+' is compiled,please test..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled'+'server path is '+'/home/swift')
                Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled successfully..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled')
                shutil.rmtree(workpath, True)
                
                return 'success'
            else:
                Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled failed..')
                shutil.rmtree(workpath, True)
                return 'failed'
        except Exception,e:
            shutil.rmtree(workpath, True)
            print e
            return e
    if env=='java':
        os.chdir(workpath)
        res=os.system('ant')
        if res==0:
            l=sourcedir.split('/')
            projname=l[len(l)-2]
            files=svndiff.showdiff(sourcedir+'/trunk',workpath)
            sshupload.uploadfile(projname,files, '192.168.10.166','/home/swift/addtional/', 'swift', 'wjffsxka')
            Sendmail.sendtogroup('testing', 'version '+tagname, 'version '+tagname+' is compiled,please test..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled'+'server path is '+'/home/swift')
            Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled successfully..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled')
            shutil.rmtree(workpath,True)
            return 'success'
        else:
            Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled failed..')
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
    global workpath
    for filename in iterfindfiles(workpath, "*.csproj"): 
        print filename
if __name__=="__main__":
    compile('.net','.net service test','{"tagname":"123","userpwd":"!@WSXadjSwift","language":".net","svnurl":"https://192.168.10.110/svn/svn-air-test/","username":"swift"}')
    #compile('.net','.net service test')
    #compile('.net','.net service test')