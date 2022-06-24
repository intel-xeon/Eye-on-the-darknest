import getopt
import sys
import os
import socket
import time
import shutil

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
    




def usage():
    print("\n\n-h --help\t\tshow help\n-f --file\t\tset url file\n-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")\n-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)\n-o --onlyscope\t\tdoesn't search external link found in url scope\n-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)\n-p --path\t\tPath where you want save your result (Example: -p /var/www/html)\n\nUsage example:\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
arr = ["-f or --file","-q or --query","-s or --splitter","-p or --path"]
tor = False
banner = open("banner.txt",'r')
print(banner.read())
banner.close()

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
    opts, args = getopt.getopt(sys.argv[1:],"htf:q:s:op:",["help","tor""file=","query=","splitter=","onlyscope","path="])
    if (not len(sys.argv[1:])):
        usage()
        exit()
    param = ""
    for o,a in opts:
        if (o in ('-f','--file')):
            param+=" -a file="+a
            arr.remove("-f or --file")
        elif (o in ('-q','--query')):
            a = a.replace('"','\\"')
            param+=" -a string=\""+a+"\""
            arr.remove("-q or --query")
        elif (o in ('-s','--splitter')):
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
if(len(arr)>0):
    print("For go ahead you must set the following parameters:\n")
    for x in arr:
        print("==>",x)
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
