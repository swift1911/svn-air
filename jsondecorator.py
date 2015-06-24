__author__ = 'swift1911'

import json
def paramcheck(paralist,jsondata):
    def wrap(f):
        print ('inside wrap')
        def param(*args):
            j=json.loads(jsondata)
            if paralist==None:
                raise Exception('parament is none')
            elif len(j) < len(paralist):
                for k in j.keys():
                    if k in paralist:
                        paralist.remove(k)
                raise Exception('parament missing',paralist)
            else:
                for i in j.keys():
                    if i not in paralist:
                        print ('fault param',i)
                        return param
                print('param ok')
                f()
        return param
    return wrap

@paramcheck(['sid','guid'],'{"sid":"123","guid":"ffg"}')
def paramchecktest():
    print ('123')

paramchecktest()
