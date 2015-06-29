Svn-air document

Compile.py
编译入口类，读取xml文件，以及从svn上checkout项目下来进行编译，编译后返回给前端tornado框架返回给前端数据。
Jsondecode.py
Json解析类，用于json字符串的解析
Log.py
日志记录类，用于记录日志
Mongodbaction.py
Mongodb的操作类，操作mangodb的数据库。
Sendmail.py
发送邮件的类，用于发送邮件。
Service.py
Windows服务类，用于安装windows服务，封装了tor.py的main方法，有bug，服务封装了tornado的入口无法启动(其实只启动tor.py是没有任何错误的)。
Tor.py
Tornado框架入口，当windows服务无法运行时可直接运行tor.py
Svndiff.py
比较两个svn source中的地址。
Unittest.py
单元测试
Sshupload.py
Linux系统使用ssh进行文件上传
Winupload.py
Windows下使用scp.exe对文件进行上传。

