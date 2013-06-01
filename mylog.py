import time

class datalog:
    def __init__(self,filename):
        self.logfile=open(filename,'a')
       

    def enterdomainfound(self,keywords,domain):
        self.logfile.write('TIME:'+time.ctime()+'\n')
        self.logfile.write('KEYWORDS:'+ str(keywords)+'\n')
        self.logfile.write('DOMAIN:'+domain+'\n\n')

    def enterurlfound(self,keywords,domain,urls):
        self.logfile.write('TIME:'+time.ctime()+'\n')
        self.logfile.write('KEYWORDS:'+str(keywords)+'\n')
        self.logfile.write('DOMAIN:'+domain+'\n')
        self.logfile.write('URLS'+str(urls)+'\n\n')

    def close(self):
        self.logfile.close()
