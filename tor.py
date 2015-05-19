from tornado.tcpserver import TCPServer
from tornado.ioloop  import IOLoop
import compile
from xml.etree import ElementTree
import jsondecode
import Sendmail
import log

class SvnkitServer(TCPServer):  
            def handle_stream(self, stream, address): 
                print "New connection :", address, stream 
                Connection(stream, address) 
                print "connection num is:", len(Connection.clients)
class Connection(object):
            clients = set()  
            def __init__(self, stream, address): 
                Connection.clients.add(self) 
                self._stream = stream  
                self._address = address  
                self._stream.set_close_callback(self.on_close)  
                self.read_message()  
                print "A new user has connected.", address
                
            def read_message(self):  
                self._stream.read_until('\n', self.send_message)
            def send_message(self, data):
                logger=log.getlogger()
                logger.info(data)
                print data
                if jsondecode.jsondecode(data,'language')==".net":
                        #self._stream.write_to_fd(".net")
                    self._stream.write_to_fd(compile.compile('.net',jsondecode.jsondecode(data,'tagname'),data))
                    self.read_message()
                elif jsondecode.jsondecode(data,'language')=="java":
                    self._stream.write_to_fd(compile.compile('java', jsondecode.jsondecode(data,'tagname'),data))
                    self.read_message()
                elif jsondecode.jsondecode(data,'language')=="testok":
                    Sendmail.sendtogroup('run', 'version '+jsondecode.jsondecode(data,'tagname'), 'version '+jsondecode.jsondecode(data,'tagname')+' is test ok,please run it')
                    self._stream.write_to_fd('ok')
                    self.read_message()
                else:
                    self._stream.write_to_fd("no support language")
                    self.read_message()
            def on_close(self):
                print "A user has lost connection.", self._address
                Connection.clients.remove(self)
def listen(port):
    server = SvnkitServer()
    server.listen(port)
    IOLoop.instance().start()
def stoplisten():
    IOLoop.instance().stop()
    
if __name__=="__main__":
    xml_file='config.xml'
    xml=ElementTree.ElementTree(file=xml_file).getroot()
    port=xml.find('localport').text
    listen(port)
