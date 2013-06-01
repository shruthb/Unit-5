import random

cloudfile=open("Cloud Computing.txt")
cloudlist=[line.strip() for line in cloudfile.readlines()]
#print cloudlist ,"\n"

mobilefile=open("Mobile Computing.txt")
mobilelist=[line.strip() for line in mobilefile.readlines()]
#print mobilelist,"\n"

socialfile=open("Social Computing.txt")
sociallist=[line.strip() for line in socialfile.readlines()]
#print sociallist,"\n"

langfile=open("Audio, Speech, and Language Processing.txt")
langlist=[line.strip() for line in langfile.readlines()]
#print langlist,"\n"

securityfile=open("Security and Privacy.txt")
securitylist=[line.strip() for line in securityfile.readlines()]
#print securitylist,"\n"


filename ='keysimulated.tab' 
testfilename ='keyinput.tab' 

def create_test_dataset(fname, n, train):
    f = open(fname, 'w')
    atts = ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5', 'keyword6', 'keyword7', 'keyword8', 'technology']
    types = ['d'] * 9
    types[8] = 'd'
    cls = [''] * 9
    cls[8] = 'class'
    
    f.write('\t'.join(atts) + '\n')
    f.write('\t'.join(types) + '\n')
    f.write('\t'.join(cls) + '\n')

    if (train):
        cloud = "Cloud Computing"
        mob = "Mobile Computing"
        social = "Social Computing"
        lang = "Audio, Speech, and Language Processing"
        sec = "Security and Privacy"
    else:
        cloud =''
        mob=''
        social=''
        lang=''
        sec=''

    for i in range(n):
        line = random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' +random.choice(cloudlist) + '\t' + cloud + '\n\n\n'
        f.write(line)

    for i in range(n):
        line = random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' +random.choice(mobilelist) + '\t' + mob + '\n\n\n'
        f.write(line)

                                                                                                                                                                                                                                                                                                                       
    for i in range(n):
        line = random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' +random.choice(sociallist) + '\t' + social + '\n\n\n'
        f.write(line)

                                                                                                                                                                                                                                                                                                                       
    for i in range(n):
        line = random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' +random.choice(langlist) + '\t' + lang + '\n\n\n'
        f.write(line)

    for i in range(n):
        line = random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' +random.choice(securitylist) + '\t' + sec + '\n\n\n'
        f.write(line)


    f.close()

if __name__ == '__main__' :
    create_test_dataset(filename, 100, True)
    create_test_dataset(testfilename, 10, False)

