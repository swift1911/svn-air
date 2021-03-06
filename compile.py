
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
from mongodbaction import mongodbaction
import svndiff
ret=''
workpath=''
sourcedir=''
username=''
pwd=''
defpath=os.getcwd()
push=''


def exportfile(jsonstr,remotepath):
    global workpath
    global sourcedir
    global username
    global pwd
    global push
    logger=log.getlogger()
    xml_file=sys.path[0]+'\\config.xml' 
    xml=ElementTree.ElementTree(file=xml_file).getroot()
    sourcedir=jsondecode.jsondecode(jsonstr,'svnurl')
    l=sourcedir.split('/')
    projname=l[len(l)-2]
    workpath=xml.find('temppath').text+projname
    username=jsondecode.jsondecode(jsonstr,'username')
    pwd=jsondecode.jsondecode(jsonstr,'userpwd')
    push=jsondecode.jsondecode(jsonstr,'push')
    try:
        r=svn.remote.RemoteClient(sourcedir+remotepath,username,pwd)
        r.checkout(workpath)
        #r.run_command('commit')
    except Exception,e:
        logger.info(e)
        print e
        return e
    #shutil.rmtree(os.getcwd()+'\\svn temp')
def compile(env,tagname,jsonstr):
    global workpath
    global username
    global pwd
    global push
    global ret
    global sourcedir 
    logger=log.getlogger()
    logger.info(os.getcwd())
    logger.info(jsonstr)
    if env=='.net':
        try:
            exportfile(jsonstr,'trunk')
            getprojfilepath()
            print ret
            logger.info(ret)
            os.chdir(ret)
            l=sourcedir.split('/')
            projname=l[len(l)-2]
            if push==0:
                cmd='msbuild /p:Configuration=Release;VisualStudioVersion=12.0 /p:WebProjectOutputDir=%s\\192.168.10.62\\upload\\%s /p:OutputPath=%s\\192.168.10.62\\upload\\%s\\bin'%('\\',projname,'\\',projname) 
            if push==1:
                cmd='msbuild /p:Configuration=Release;VisualStudioVersion=12.0'
            print cmd
            res=os.system(cmd)
            if push==0:
                cmd='msbuild /p:Configuration=Release;VisualStudioVersion=12.0 /p:WebProjectOutputDir=c:\\Release\\%s /p:OutputPath=c:\\Release\\%s\\bin'%(projname,projname) 
                os.system(cmd)
                cmd='msbuild /p:Configuration=Release;VisualStudioVersion=12.0'
                os.system(cmd)
            if res==0:              
                r=svn.remote.RemoteClient(sourcedir,username,pwd)
                files=svndiff.showdiff(sourcedir+'/tags/original',workpath)  
                winupload.winup(0,'\\192.168.10.62\\upload\\backup', files, projname,tagname)
                winupload.winup(1,'c:\\zz',files,projname,tagname)
                sshupload.uploadfile(projname, files, '172.18.7.88', '/home/swift/','swift', '1234qwer')
                path=['trunk','tags/'+tagname]
                print r.run_command('copy',[sourcedir+'trunk', sourcedir+'tags/'+tagname+'_compiled','-m','copy'])
                dbclient=mongodbaction()
                dbclient.insertlog(projname,username,'compile',tagname)        
                if push==0:
                    Sendmail.sendtogroup('test', 'version '+tagname, 'version '+tagname+' is compiled,please test..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled')
                Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled successfully..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled')
                return 'success'
            else:
                Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled failed..')
                return 'failed'
        except Exception,e:
            print e
            return e
    if env=='java':
        exportfile(jsonstr,'trunk')
        os.chdir(workpath)
        res=os.system('ant')
        if res==0:
            l=sourcedir.split('/')
            projname=l[len(l)-2]
            files=svndiff.showdiff(sourcedir+'/trunk',workpath)
            sshupload.uploadfile(projname,files, '192.168.10.166','/home/swift/addtional/', 'swift', 'wjffsxka')
            Sendmail.sendtogroup('testing', 'version '+tagname, 'version '+tagname+' is compiled,please test..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled'+'server path is '+'/home/swift')
            Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled successfully..'+'path : '+sourcedir+"/tags/"+tagname.encode()+'_compiled')
            #shutil.rmtree(workpath, True)
            return 'success'
        else:
            Sendmail.sendtogroup('develop', 'version '+tagname, 'version '+tagname+' is compiled failed..')
            #shutil.rmtree(workpath, True)
            return 'failed'
    if env=='testok':
        ssdir=jsondecode.jsondecode(jsonstr,'svnurl') 
        l=ssdir.split('/')
        projname=l[len(l)-2]    
        Sendmail.sendtogroup('run', 'version '+tagname, 'project:'+projname+' version: '+tagname+' is test ok,please pull it')
        dbclient=mongodbaction()
        dbclient.insertlog(projname,jsondecode.jsondecode(jsonstr,'username'),'test ok',tagname)
    if env=='run':
        exportfile(jsonstr,'tags/'+tagname)
        getprojfilepath()
        os.chdir(ret)
        l=sourcedir.split('/')
        projname=l[len(l)-2]
        cmd='msbuild /p:Configuration=Release;VisualStudioVersion=12.0 /p:WebProjectOutputDir=%s\\192.168.10.165\\share\\%s /p:OutputPath=%s\\192.168.10.165\\share\\%s\\bin'%('\\',projname,'\\',projname)
        res=os.system(cmd)
        print workpath
        dbclient=mongodbaction()
        dbclient.insertlog(projname,username,'go online',tagname)
        if res==0:
            Sendmail.sendtogroup('run', 'version '+tagname, 'project:'+projname+' version '+tagname+' is push ok,please run it')
        else:
            Sendmail.sendtogroup('run', 'version '+tagname, 'project:'+projname+' version '+tagname+' is push error')
def iterfindfiles(path, fnexp):
    global ret
    ret=''
    for root, dirs, files in os.walk(path): 
        for filename in fnmatch.filter(files, fnexp): 
            yield os.path.join(root, filename)
            ret+=root
def getprojfilepath():
    global workpath
    for filename in iterfindfiles(workpath, "*.sln"):
        print filename
if __name__=="__main__":
    compile('.net','.net service test','{"tagname":"123","userpwd":"!@WSXadjSwift","language":".net","svnurl":"https://192.168.10.110/svn/svn-air-test/","username":"swift"}')