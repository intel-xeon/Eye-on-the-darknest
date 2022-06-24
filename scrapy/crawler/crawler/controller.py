import getopt,sys,os


def usage():
    print("\n-h --help\t\tshow help\n-f --file\t\tset url file\n-q --query\t\tset your custom keyword(Exaple: \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\")\n-s --splitter\t\tset a splitter char (Example: splitter=\"/\" make --query=\"string1/string2\" two different keyword)\n-o --onlyscope\t\tdoesn't search external link found in url scope\n-t --tor\t\ttraffic over tor network(Make sure you have tor installed with port 9050 open)\n-p --path\t\tPath where you want save your result (Example: -p /var/www/html)\n\nUsage example:\tpython3 controller.py -f url.txt -q \"String1/String2/String3/String4_part1*String4_part2/Stri ng5\" -s \"/\" -o -p /var/www/html \r\n")
arr = ["-f or --file","-q or --query","-s or --splitter","-p or --path"]
tor = False
banner = open("banner.txt",'r')
print(banner.read())
banner.close()


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
            param+=" -a path=\""+a+"\""
            arr.remove("-p or --path")
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
    command="torify scrapy crawl search"+param
else:
    command="scrapy crawl search"+param
os.system(command)
