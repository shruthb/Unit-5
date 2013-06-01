import Orange
import sys
import mylog
from pymongo import Connection
import mycreatedataset

connectiontomongo = Connection()  #making a connection
db = connectiontomongo.url_database   #getting a database
collection = db.url_collection    #getting a collection

def queryfile():
    f = open('queried.tab', 'w')
    atts = ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5', 'keyword6', 'keyword7', 'keyword8', 'technology']
    types = ['d'] * 9
    types[8] = 'd'
    cls = [''] * 9
    cls[8] = 'class'
    
    f.write('\t'.join(atts) + '\n')
    f.write('\t'.join(types) + '\n')
    f.write('\t'.join(cls) + '\n')
    f.close()

def appendtoqueryfile(words,c):
    f=open("queried.tab","a")
    f.write('\t'.join(words)+ '\t'+ c + '\n\n')
    f.close()

def checkifvalid(words):
    for i in words:
        if(( i in mycreatedataset.cloudlist)|(i in mycreatedataset.mobilelist)|(i in mycreatedataset.sociallist)|(i in mycreatedataset.langlist)|(i in mycreatedataset.securitylist)):
            valid=1
        else:
            #print i,"not der"
            valid=0
        return valid


def queryingdomain():
    conti=1
    while(conti):
        x=raw_input('enter the keywords(recommended 8 to get accurate results):')
        x=x.lower()
        words=x.split(',')
        if len(words)>8:
            print"warning: too many keywords given \n domains may overlapp\n"
        val=checkifvalid(words)
        if(val):
      

            f=open('mysimulated.tab','a')
        
            f.write('\t'.join(words)+'\t\n\n')
#if u dont close it wont write
            f.close()
            data= Orange.data.Table('mysimulated.tab') 
            classifier = Orange.classification.bayes.NaiveLearner(data)
            c=classifier(data[len(data)-1])
    
            data[len(data)-1]['technology']=c
            val=data[len(data)-1]['technology'].value
            appendtoqueryfile(words,val)
        
            doc.enterdomainfound(words,val)
            print 'The keywords %s belong to the domain of : %s \n' % (words,c)
            satisfied=raw_input("are u satisfied with the domain returned?(y/n)")
            print type(satisfied)
            if ((satisfied==('y'))|(satisfied == '1')):
                print 'the list of urls dat match the domain %s and the keywords %s are'% (c,words )
                for i in collection.find( {'key words' :{"$in" :words} }):
                
                    print i['url']
            elif ((satisfied=='n')| (satisfied=='0')):
                print'try gain with different keywords or repeat'
            else:
                print'invalid input'
        else:
            print"invalid input"

        try:       
            conti=int(raw_input('do you want to continue(1/0)\n'))
        except:
            print("TypeError")


def insertIntoDb(url,keywords,domain):
    data = {"domain":domain,"keywords":keywords,"url":url}
    collection.insert(data)

def querydomain(keywords):
    f = open('keysimulated.tab','a')
    f.write('\t'.join(keywords)+'\t\n\n')
    f.close()
    doc = mylog.datalog('logs.txt')
    #queryfile()
    #appendtoqueryfile(keywords)
    data = Orange.data.Table('keysimulated.tab')
    classifier = Orange.classification.bayes.NaiveLearner(data)
    #data2 = Orange.data.Table('queried.tab')
    c = classifier(data[-1])
    val = c.value
    appendtoqueryfile(keywords,val)
    doc.enterdomainfound(keywords,val)
    #logging.info(str(keywords)+" "+val)
    doc.close()
    res = []
    for each in collection.find({"keywords" :{"$in" :keywords},"domain" : val},{"url":1,"_id":0}) :
        res.append(str(each["url"]))
    return val,res
    

insert_in_database=[{"domain":"cloud computing","keywords":["cloud computing","cloud services","data centers","open systems"],"url":"http://url1.com"}, \
                    {"domain":"cloud computing","keywords":["virtualisation","cloud services","parallel computing","peer-to-peer computing"],"url":"http://url2.com"}, \
                    {"domain":"cloud computing","keywords":["data privacy","distributed computing",],"url":"http://url3.com"}, \
                    {"domain":"audio,speech and language processing","keywords":["speech","microphone","audio coding","distortion","speech enhancement"],"url":"http://url4.com"}, \
                    {"domain":"audio,speech and language processing","keywords":["noise reduction","dereverberation","videoconferencing"],"url":"http://url5.com"}, \
                    {"domain":"audio,speech and language processing","keywords":["audio coding","mixed signals","speech","acoustic correlation"],"url":"http://url6.com"}, \
                    {"domain":"security and privacy","keywords":["cyberattack","software vulnerabilities","identity management","cryptography"],"url":"http://url7.com"},\
                    {"domain":"security and privacy","keywords":["data privacy","antivirus","cryptography"],"url":"http://url8.com"},\
                    {"domain":"security and privacy","keywords":["security","virus","computer crime","cryptography","intrusion tolerance"],"url":"http://url9.com"},\
                    {"domain":"mobile computing","keywords":["mobile computing","wireless communication","long term evolution"],"url":"http://url10.com"},\
                    {"domain":"mobile computing","keywords":["interference","long term evolution","smart phones","global positioning system","energy consumption"],"url":"http://url11.com"},\
                    {"domain":"mobile computing","keywords":["Scattering","signal to noise ratio","ad hoc networks","sporadic connectivity"],"url":"http://url12.com"},\
                    {"domain":"social computing","keywords":["customer loyalty","social behavior","intelligent agents","social informatics","informatics","psychology"],"url":"http://url13.com"},\
                    {"domain":"social computing","keywords":["artificial intelligence","data mining","data collectiont","internet shopping","electronic commerce"],"url":"http://url14.com"},\
                    {"domain":"social computing","keywords":["pattern classification","data mining","sentiment analysis"],"url":"http://url15.com"},\
                    ]


if __name__=="__main__":
    #db.drop_collection("url_collection")
    #collection.insert(insert_in_database)

    doc=mylog.datalog('logs.txt')
    queryfile()
    queryingdomain()
    '''x = raw_input('enter the 8 keywords:') #min 4 for proper classification
    words = x.split(',') #list
    a,b = querydomain(words)
    print a
    print b''' 
    doc.close()

