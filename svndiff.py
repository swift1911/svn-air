import svn
import subprocess


def showdiff(path1,path2):
    cmd='svn diff --summarize --new %s --old %s'%('"'+path1+'"',path2)
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.stdout.readline():
        print p.stdout.readline()
if __name__=="__main__":
    showdiff('c:\\svn-air-test\\trunk', 'https://192.168.10.110/svn/svn-air-test/trunk')
