import win32serviceutil
import win32service
import win32event
import tor
from xml.etree import ElementTree
import sys


class svnair(win32serviceutil.ServiceFramework): 

    _svc_name_ = "Svn-air tService"
    _svc_display_name_ = "Svn-air Service"
    _svc_description_ = "Svn-air background Service"
    __port=''
    
    def __init__(self, args): 
        win32serviceutil.ServiceFramework.__init__(self, args) 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.isAlive = True
        xml_file=sys.path[0]+'\\config.xml'
        xml=ElementTree.ElementTree(file=xml_file).getroot()
        self.__port=xml.find('localport').text
        
    def _getLogger(self):
        import logging
        import os
        import inspect

        logger = logging.getLogger('[SvnkitService]')
        
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        return logger

    def SvcDoRun(self):
        self.logger.info("svc do run....")
        self.logger.info ("Server start ......")
        
        tor.listen(self.__port)
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        
            
    def SvcStop(self):
        self.logger.info("svc do stop....")
        tor.stoplisten()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) 
        win32event.SetEvent(self.hWaitStop) 
        self.isAlive = False
    
if __name__=='__main__': 
    win32serviceutil.HandleCommandLine(svnair)
