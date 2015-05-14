import json

def jsondecode(jstr,col): 
    j=json.loads(jstr)
    return j[col]

if __name__=="__main__":
    jstr='{"userpwd":"!@WSXadjSwift","language":".net","svnurl":"https://192.168.10.110/svn/svn-air-test/","username":"swift"}'
    print jsondecode(jstr,"language")