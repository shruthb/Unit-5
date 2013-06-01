import sys
import re
import urllib2
import urlparse
import keyclassifier
import logging
import threading
import Queue
from bs4 import BeautifulSoup

logging.basicConfig(filename="urllog.log", level=logging.INFO)

class ieeecrawler(threading.Thread) :
    def __init__(self, topic, url='', pages=3):
        threading.Thread.__init__(self)
        self.createCrawlSet(topic, url, pages)
        self.crawled_articles = set([])
        self.articles = set([])
        self.keywords = set([])
        self.topic = topic
        self.kfile = open(topic+".txt", "w")
        self.artqueue = Queue.Queue()
        self.pgqueue = Queue.Queue()
        self.kloc = threading.Lock()
        self.aloc = threading.Lock()
        #self.writewords = []

    def writeKeywords(self) :
        for keyword in self.keywords :
            self.kfile.write(keyword+'\n')
            print keyword
        self.kfile.close()

    def createCrawlSet(self, topic, url, pages) :
        #topic type - 1.url 2.some topic like mobile computing
        #need to check if pages is +ve and within some limit, topic is sensible?
        self.pages = []
        if url : 
            basic = "http://ieeexplore.ieee.org{0}"
            try:
                response = urllib2.urlopen(url)
                content = response.read()
            except:
                print "could not open %s" % crawling
                #exit
            soup = BeautifulSoup(content)
            for ul in soup.findAll("ul", id=re.compile("pi-201[23]")) : #\d")) :
                for a in ul.findAll("a", href=re.compile("^/")) :
                    self.pages.append(basic.format(a["href"]))
            
        else :
            queryText = topic.lower().replace(" ", "+")
            basic = "http://ieeexplore.ieee.org/search/searchresult.jsp?ranges%3D1997_2013_p_Publication_Year%26queryText%3D{0}&addRange=2010_2013_Publication_Year&pageNumber={1}&resultAction=REFINE#"
            for i in range(1,pages+1) :
                self.pages.append(basic.format(queryText,i))         
            
        self.printlinks("links to pages with links to articles:\n", self.pages)

    def printlinks(self, line, links) :
        print line
        for link in links :
            print link
        print

    def keyword(self, tag) :
        return tag.has_key("data-keyword")

    def findKeywords(self, soup) :
        '''finds the keywords for an article in the page'''
        self.kloc.acquire()
        artkeys = set([])
        for key in soup.find_all(self.keyword) :
            try :
                k = str(key["data-keyword"]).lower()
                artkeys.add(k)
                self.keywords.add(k)
                #print k
            except UnicodeEncodeError :
                continue
        self.kloc.release()
        return artkeys

    def findArticleLinks(self, soup) :
        '''find all the links to articles in the page'''
        self.aloc.acquire()
        basic = "http://ieeexplore.ieee.org{0}"
        for each in soup.find_all("a", href=re.compile("/xpl/articleDetails.jsp\?(tp=&)?arnumber=\d+.*")) :
            url = each["href"].replace("articleDetails", "abstractKeywords")
            url = basic.format(url)
            if url not in self.crawled_articles and url not in self.articles :
                self.articles.add(url)
                self.artqueue.put(url)
        self.aloc.release()
        #self.printlinks("\nlinks to articles (keyword) :\n", self.articles) #change in other thread exception
    
    def run(self) :
        'creates threads for crawling and fills the queue'
        self.pgqueue
        for i in range(5) :
            t = threading.Thread(target=self.pagecrawl)
            t.setDaemon(True)
            t.start()
            
        #populate queue with data
        for purl in self.pages :
            self.pgqueue.put(purl)
        
        #spawn a pool of threads, and pass them queue instance
        for i in range(5) :
            t = threading.Thread(target=self.articlecrawl)
            t.setDaemon(True)
            t.start()

        self.pgqueue.join()
        '''for aurl in self.articles :
            self.artqueue.put(aurl)'''

        #wait on queue till everything has been processed
        self.artqueue.join()

        print "done :\n"
        self.writeKeywords()
        

    def articlecrawl(self) : #, url) :
        #for crawling in self.articles :
        while True :
            crawling = self.artqueue.get()
            print "CRAWLING ARTICLE :", crawling
            logging.info("crawling : "+crawling+"\n")
            try :
                response = urllib2.urlopen(crawling)
                content = response.read()
            except :
                print "could not open %s" % crawling
                logging.warning("could not open %s" % crawling)
                continue
            finally :
                self.crawled_articles.add(crawling)
                #self.articles.remove(crawling) #exception set changed during iteration
            soup = BeautifulSoup(content)
            artkeys = self.findKeywords(soup)
            keyclassifier.insertIntoDb(crawling, list(artkeys), self.topic)#now store url of article,its artkeys,domain
            self.artqueue.task_done()            
            

    def pagecrawl(self) :
        #for crawling in self.pages :
        while True :
            crawling = self.pgqueue.get()
            print "CRAWLING PAGE :", crawling
            url = urlparse.urlparse(crawling)
            try:
                response = urllib2.urlopen(crawling)
                content = response.read()
            except:
                print "could not open %s" % crawling
                continue
            soup = BeautifulSoup(content)
            self.findArticleLinks(soup)
            self.pgqueue.task_done()
            

if __name__=='__main__':
    topic = ["Cloud Computing","Social Computing"]
    t = []
    for each in topic :
        t.append( ieeecrawler(each, pages = 5) )
    t.append( ieeecrawler("Audio, Speech, and Language Processing", url="http://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10376" ))
    t.append( ieeecrawler("Security and Privacy", url="http://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8013" ))
    t.append( ieeecrawler("Mobile Computing", url="http://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=7755" ))
    for each in t :
        each.start()

    for each in t:
        each.join()

#http://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Social%20Computing
#http://ieeexplore.ieee.org/search/searchresult.jsp?ranges%3D1997_2013_p_Publication_Year%26queryText%3Dcloud+computing&addRange=2010_2013_Publication_Year&pageNumber=1&resultAction=REFINE#
#http://ieeexplore.ieee.org/search/searchresult.jsp?ranges%3D1997_2013_p_Publication_Year%26queryText%3Dsocial+computing&addRange=2010_2013_Publication_Year&pageNumber=2&resultAction=REFINE#
