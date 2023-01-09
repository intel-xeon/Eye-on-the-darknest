import getopt
import sys
import os
import socket
import time
import shutil
import random
import ast

#Da implementare il parametro regex nello spidervdbr

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
        error.append("[REGEX] Only integer number is accepted. Error on '"+regex+"'")
        return error
    elif(int(regex)>maximum or int(regex)<1):
        error.append("[REGEX] MIN accpeted:1 MAX accepted:"+str(maximum)+" your value:"+regex+"")
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
            error.append("[REGEX] More items have been included than are present max accepted:"+str(maximum)+" your items:"+str(len(l)))
            return error
        for x in l:
            r = isvalidregexfieldsingle(maximum,x,error)
            if(len(r)>0):
                return error
    return error




def isvalidtemplate(maximum,t):
    error = []
    if (len(t)==0):
        error.append("[TEMPLATE] Template field can't be empty..")
        return error
    t = t.split(",")
    if(len(t)>maximum):
        error.append("[TEMPLATE] More items have been included than are present max accepted:"+str(maximum)+" your items:"+str(len(t)))
        return error
    for x in t:
        if(not x.isdigit()):
            error.append("[TEMPLATE] Only integer number is accepted. Error on '"+x+"'")
            return error
        if(int(x)>maximum or int(x)<1 ):
            error.append("[TEMPLATE] MIN accpeted:1 MAX accepted:"+str(maximum)+" your value:"+x+"")
            return error
    return error
        




def usage():
    #print("\n\n-h --help\t\tshow help\n-f --file\t\tset url file\n-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")\n-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)\n-o --onlyscope\t\tdoesn't search external link found in url scope\n-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)\n-p --path\t\tPath where you want save your result (Example: -p /var/www/html)\n\nUsage example:\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
    print("--generatesplitter\tGenerate a perfect splitter char \n\r\t\t\tUsage Example: --generate-splitter [YOUR_SEARCH_STRING_AND_REGEX] (concatenated without any splitter)\n\r\t\t\tExample of generation for words foo and foo2: --generate-splitter \"foofoo2\"")
    print()
    print("-h --help\t\tshow help")
    print("-f --file\t\tset url file")
    print("-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")")
    print("-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)")
    print("-o --onlyscope\t\tdoesn't search external link found in url scope")
    print("-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)")
    print("-p --path\t\tPath where you want save your result (Example: -p /var/www/html)")
    print("-z --template\t\tChoose a template (Example: -t 1,3)")
    print("-l --list\t\tprint a list of available template")
    print("-x --regex\t\tmarks the location of your RegExpr in the query parameter (Example: -x 1 OR -x 1,3)")
    print("--lookup\t\tlookup a template")
    print("--create\t\tcreate/modify a template")
    print("--delete\t\tdelete a template")
    print("\n")
    print("Usage example1:\t\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
    print("Usage example2:\t\tpython3 controller.py -f url.txt -q \"your_regex_1/String2/your_regex3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html -x 1,3")
    print("WARNING:\nmake sure you don't have the char splitter in your regex if you use them")
    print("If you choose template-based search, you can't set a query and splitter.. they will be ignored.\n\n")
arr = ["-f or --file","-q or --query","-s or --splitter","-p or --path"]
tor = False
banner = open("banner.txt",'r')
print(banner.read())
banner.close()

def creation(list_template):
    listtemplate(list_template)
    name = input("Choose a name for template: ")
    if(name in list_template):
        c = input("This template are already present, do you want overwrite it?(y/other) ")
        if(c.lower() == 'y'):
            regex = input ("Insert your regex: ")
            list_template[name]=regex
            f = open("template.txt",'w')
            f.write(str(list_template))
            f.close()
            print("List updated!")
        else:
            print("exit...")
            return
    else:
        regex = input ("Insert your regex: ")
        list_template[name]=regex
        f = open("template.txt",'w')
        f.write(str(list_template))
        f.close()
        print("List updated!")

def generation():
    string = input("Insert your query: ")
    string = string.strip()
    if(len(string)==0):
        return "The string cannot be empty..."
    i = 0
    while True:
        r = ["~","!","@","#","$","%","^","&","(",")","-","_","+","=","{","}","]","[","|","'",",",",",".",",","/","?",";",":","<"]
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
                x+=random.choice(rQF)
                if (x not in string):
                    return x
        i+=1

def checktemplate(opts):
    for o,a in opts:
        if(o in ('-z','--template')):
            return True
    return False
        
def readtemplate():
    f = open("template.txt",'r')
    r = f.read()
    f.close()
    return ast.literal_eval(r)
    
def tutorialregex():
    print("REGEX ERROR:")
    print("="*50)
    print("Use the parameter -x/--regex as follows:\nExample1:  -x 1,2,3\nExample2 --regex 1,2,3")
    print("="*50)

def tutorialtemplate():
    print("TEMPLATE ERROR:")
    print("="*50)
    print("Use the parameter -z/--template as follows:\nExample1:  -z 1,2,3\nExample2 --template 1,2,3")
    print("="*50)

def listtemplate(lista):
    print("="*50)
    print("TEMPLATE AVAILABLE\n\n")
    i = 1
    for x in lista:
        print(str(i)+")",x)
        i+=1
    print("="*50)

def delete(list_template):
    if(len(list_template)==0):
        print("There are no templates to delete...")
        return
    listtemplate(list_template)
    i = input("choose the template index to delete: ")
    if(not i.isdigit()):
        print("Only integer number accepted")
        return
    i = int(i)
    if(i>len(list_template) or i<1):
        print("[ERROR]==> Minimum acceptable value: 1 maximum value: "+str(len(list_template)),"exit..")
        return
    h = 0
    for x in list_template:
        h+=1
        if(i==h):
            c = input("Are you sure you want to delete the item "+x+"? (y/other)")
            if(c.lower()=='y'):
                list_template.pop(x)
                f = open("template.txt","w")
                f.write(str(list_template))
                f.close()
                print("Item "+x+" deleted")
                return
            else:
                break
    print("No item deleted")
    
def lookup(list_template):
    if(len(list_template)==0):
        print("There are no templates to view...")
        return
    listtemplate(list_template)
    i = input("choose the template index to lookup: ")
    if(not i.isdigit()):
        print("Only integer number accepted")
        return
    i = int(i)
    if(i>len(list_template) or i<1):
        print("[ERROR]==> Minimum acceptable value: 1 maximum value: "+str(len(list_template)),"exit..")
        return
    h = 0
    for x in list_template:
        h+=1
        if(i==h):
            print("NAME:"+x+"\nREGEX:\n")
            print(repr(list_template[x]))
            print("\n")
            return
    

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

template = False

try:
    opts, args = getopt.getopt(sys.argv[1:],"htf:q:s:op:x:gz:l",["help","tor","file=","query=","splitter=","onlyscope","path=","regex=","generatesplitter","template=","list","create","delete","lookup"])
    if (not len(sys.argv[1:])):
        usage()
        exit()
    param = ""
    regex="False"
    keyword = ""
    splitter = ""
    list_template = readtemplate()
    t = ""
    template = checktemplate(opts)
    for o,a in opts:
        if (o in ('-f','--file')):
            param+=" -a file="+a
            arr.remove("-f or --file")
        elif (o in ('--create')):
            creation(list_template)
            exit()
        elif (o == '--lookup'):
            lookup(list_template)
            exit()
        elif (o in ('--delete')):
            delete(list_template)
            exit()     
        elif (o in ('-z','--template')):
            t = a
            arr.remove("-s or --splitter")
            arr.remove("-q or --query")
            param+=" -a template=\""+t+"\""
        elif (o in ('--generatesplitter')):
            print("You can use this as splitter ==> "+generation())
            exit()
        elif (o in ('-l','--list')):
            listtemplate(list_template)
            exit()
        elif (o in ('-q','--query')):
            if(not template):
                keyword = a
                keyword = keyword.replace('"','\\"')
                param+=" -a string=\""+a+"\""
                arr.remove("-q or --query")
        elif (o in ('-s','--splitter')):
            if(not template):
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
            if(not template):
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
if(template):
    error = isvalidtemplate(len(list_template),t)
    if(len(error)>0):
        for x in error:arr.append(x)
        tutorialtemplate()
else:
    error = isvalidregexfield(0,splitter,keyword,regex,error)
    if(len(error)>0 and not regex=="False"):
        for x in error:arr.append(x)
        tutorialregex()


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
