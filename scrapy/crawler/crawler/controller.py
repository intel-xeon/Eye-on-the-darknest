import getopt
import sys
import os
import socket
import time
import shutil
import random

#Da implementare il parametro regex nello spider

def torEnabled():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = s.connect_ex(("127.0.0.1",9050))
    if(result==0):
        s.close()
        return True
    else:
        s.close()
        return False

def initpath(path):
    shutil.copyfile("result/index.html", path+"index.html")
    f = open(path+"result.json","w")
    f.write("{\"data\":[]}")
    f.close()



        
def isvalidregexfieldsingle(maximum,regex,error):
    if(not regex.isdigit()):
        error.append("Only integer number is accepted. Error on '"+regex+"'")
        return error
    elif(int(regex)>maximum):
        error.append("Index out of rangemax accepted:"+str(maximum)+" your value:"+regex+"")
        return error
    return error

def isvalidregexfield(maximum,splitter,string,regex,error):
    if(len(splitter)==0):
        return error
    if(',' not in regex):
        isvalidregexfieldsingle(len(string.split(splitter)),regex,error)
    else:
        l = string.split(splitter)
        maximum = len(l)
        l = regex.split(",")
        if(len(l)>maximum):
            error.append("More items have been included than are present max accepted:"+str(maximum)+" your items:"+str(len(l)))
            return error
        for x in l:
            r = isvalidregexfieldsingle(maximum,x,error)
            if(len(r)>0):
                return error
    return error



def usage():
    #print("\n\n-h --help\t\tshow help\n-f --file\t\tset url file\n-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")\n-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)\n-o --onlyscope\t\tdoesn't search external link found in url scope\n-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)\n-p --path\t\tPath where you want save your result (Example: -p /var/www/html)\n\nUsage example:\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
    print("--generate-splitter\tGenerate a perfect splitter char \n\r\t\t\tUsage Example: --generate-splitter [YOUR_SEARCH_STRING_AND_REGEX] (concatenated without any splitter)\n\r\t\t\tExample of generation for words foo and foo2: --generate-splitter \"foofoo2\"")
    print()
    print("-h --help\t\tshow help")
    print("-f --file\t\tset url file")
    print("-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")")
    print("-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)")
    print("-o --onlyscope\t\tdoesn't search external link found in url scope")
    print("-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)")
    print("-p --path\t\tPath where you want save your result (Example: -p /var/www/html)")
    print("\n")
    print("Usage example1:\t\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
    print("Usage example2:\t\tpython3 controller.py -f url.txt -q \"your_regex_1/String2/your_regex3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html -x 1,3")
    print("WARNING:\nmake sure you don't have the char splitter in your regex if you use them")
arr = ["-f or --file","-q or --query","-s or --splitter","-p or --path"]
tor = False
banner = open("banner.txt",'r')
print(banner.read())
banner.close()

def generation(string):
    string = string.strip()
    if(len(string)==0):
        return "The string cannot be empty..."
    i = 0
    while True:
        r = ["~","!","@","#","$","%","^","&","*","(",")","-","_","+","=","{","}","]","[","|","'",",",",",".",",","/","?",";",":","<",">"]
        random.shuffle(r)
        for x in r:
            for j in range(i):
                x+=random.choice(r)
            if (x not in string):
                return x
        r=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        random.shuffle(r)
        for x in r:
            for j in range(i):
                x+=random.choice(r)
                if (x not in string):
                    return x
        i+=1
        
def validatepath(path):
    app = path
    if (os.path.isfile(path)):
        path = os.path.dirname(filepath)+"/"
    if (not path[len(path)-1]=='/'):
        path+='/'
        app = path
    if (not os.path.isdir(path) and not path==''):
        try:
            os.makedirs(path)
            print("path "+path+" are not present in file system.. created!")
            time.sleep(3)
        except Exception:
            if(not os.path.isdir(path)):
                print("Impossible to create path... set path to project directory..")
                path= ""
                time.sleep(3)
            if (not os.access(path,os.W_OK)):
                print("I can't write to project directory")
                time.sleep(3)
                return -1
    if (not app==path):
        if(len(path)>0):
            print("Sorry.. but your path ("+app+") isn't availabe for permission problems.. i choose another path for you:",path)
        else:
            print("Sorry.. but your path ("+app+") isn't availabe for permission problems.. result will be saved into the project directory")
        time.sleep(3)
    return path


try:
    opts, args = getopt.getopt(sys.argv[1:],"htf:q:s:op:x:g:",["help","tor","file=","query=","splitter=","onlyscope","path=","regex=","generate-splitter="])
    if (not len(sys.argv[1:])):
        usage()
        exit()
    param = ""
    regex="False"
    keyword = ""
    splitter = ""
    for o,a in opts:
        if (o in ('-f','--file')):
            param+=" -a file="+a
            arr.remove("-f or --file")
        elif (o in ('--generate-splitter')):
            print("You can use this as splitter ==> "+generation(a))
            exit()
        elif (o in ('-q','--query')):
            keyword = a
            a = a.replace('"','\\"')
            param+=" -a string=\""+a+"\""
            arr.remove("-q or --query")
        elif (o in ('-s','--splitter')):
            splitter = a
            a = a.replace('"','\\"')
            param+=" -a splitchar=\""+a+"\""
            arr.remove("-s or --splitter")
            if(len(a)==0):
                arr.append("splitter can't be empty..")
        elif (o in ('-h','--help')):
            usage()
            exit()
        elif (o in ('-o','--onlyscope')):
            param+=" -a onlyscope=yes"
        elif (o in ('-x','--regex')):
            regex = a
            param+=" -a regex=\""+regex+"\""
        elif (o in ("-p",'--path')):
            path = validatepath(a)
            arr.remove("-p or --path")
            if(path==-1):
                arr.append("The path that you specified ("+a+") are not available. Please check the permissions and validity of the same")
            else:
                param+=" -a path=\""+path+"\""
                initpath(path)
        elif (o in ("-t",'--tor')):
            tor = True
except Exception as err:
    print(err)


error=[]

error = isvalidregexfield(0,splitter,keyword,regex,error)

if(len(error)>0 and not regex=="False"):
    print("REGEX ERROR:")
    print("="*50)
    for x in error:
        arr.append(x)
    print("Use the parameter -x/--regex as follows:\nExample1:  -x 1,2,3\nExample2 --regex 1,2,3")
    print("="*50)


if(len(arr)>0):
    print("To move forward, correct the following inconsistencies:\n")
    for x in arr:
        print("[ERROR] ==> ",x)
    exit()


if(tor):
    if(torEnabled()):
        command="torify scrapy crawl search"+param
    else:
        r = input("Tor is not enabled. You want enable? type 'y' for yes: ")
        if(r.lower()=='y'):
            print("Tryng to enable tor...")
            os.system("/etc/init.d/tor start")
            time.sleep(5)
            if(torEnabled()):
                print("Good news! Tor enabled!")
                command="torify scrapy crawl search"+param
            else:
                print("Tor not availabe, exit..")
                exit()
        else:
            print("Tor not availabe, exit..")
            exit()
else:
    command="scrapy crawl search"+param
os.system(command)
