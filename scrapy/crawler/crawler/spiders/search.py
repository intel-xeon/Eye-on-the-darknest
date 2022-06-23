from ipwhois import IPWhois
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
import threading
import urllib.request
import validators
try:
    import queue
except ImportError:
    import Queue as queue

#CONFIGURAZIONE INIZIALE


# La lista delle URL da cui attingere per segnalare i siti di phishing (1 per linea)
                                                                                       
list_url_in_line =  ["https://openphish.com/feed.txt"]
                                                                                       


thread = 20                                     # thread paralleli indipendenti che verranno eseguiti contemporaneamente
already_sign = "segnalato.txt"                  # File che conterrà la lista delle URL già segnalate.
error_sign = "errore_nella_segnalazione.txt"    # File che conterrà la lista delle URL NON segnalate                                            
smtp_server = "smtp.gmail.com"                  # smtp server
smtp_port = 587                                 # smtp port
sender_addr = "lukefireeye96@gmail.com"         # l'indirizzo email dal quale partiranno le segnalazioni
sender_pa = "pfjzracjyjmcwssu"                  # la password dell'indirizzo email dal quale partiranno le segnalazioni
trusted_email = "marsilialuca@gmail.com"        # Indirizzo email dove verrà notificato tramite email l'avvio dello script di segnalazione e della fine dello stesso


check = True
queue_url = queue.Queue()



def getWhoisString(host):
    host = socket.gethostbyname(host)
    obj = IPWhois(host)
    res=obj.lookup_whois()
    who = "<strong>WHOIS</strong><br>"+"-"*100
    for x in res:
        who+="<br>"+x+": "
        if(str(type(res[x]))=='<class \'list\'>'):
            for j in res[x]:
                who+="<br>"+str(j)
        else:
            who+=str(res[x])
    who+="<br>"+"-"*100
    return who





def avvio():
    mail_content = "Script avviato"
    sender_address = sender_addr
    sender_pass = sender_pa
    receiver_address = trusted_email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'SCRIPT AVVIATO'
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def fine():
    mail_content = "Ho finito l'esecuzione dello script"
    sender_address = sender_addr
    sender_pass = sender_pa
    receiver_address = trusted_email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'SCRIPT FINITO'
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def saveFile():
    for x in list_url_in_line:
        try:
            print("Tentando di prelevare le URL da "+x+" ..")
            with urllib.request.urlopen(x) as url:
                r = url.read().decode('utf-8')
                with open("File.txt", "a") as myfile:
                    myfile.write(r)
        except Exception as err:
            print("Non è stato possibile prelevare la lista dal sito "+x+"\n Stacktrace:",err)

def isvalid(url):
    if(validators.domain(url) == True or validators.url(url)==True):
        return True
    else:
        return False


def sendMail(recp,url):
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc
    url = url.replace(".","[.]")
    url = url.replace("https://","hxxps[:]//")
    url = url.replace("http://","hxxp[:]//")
    mail_content = "Hello,<br><br>This is to notify you of a phishing URL<br><br>Phishing URL to be taken down:  <strong>"+url+"</strong><br><br>"+getWhoisString(host)+"<br><br>Best regards,<br>Luca"
    sender_address = sender_addr
    sender_pass = sender_pa
    receiver_address = recp
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'WARNING PHISHING URL: '+url
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent to %s for %s' % (recp,url))

def filetolist(path):
	f = open(path)
	final = set(f.read().split("\n"))
	f.close()
	return list(filter(None, final))

def already(url):
    l = filetolist(already_sign)
    for x in l:
        if (url == x):
            return True
    return False

def getEmails(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        host = socket.gethostbyname(host)
        obj = IPWhois(host)
        res=obj.lookup_whois()
    except Exception as err:
        print("[KO] ==> Impossibile segnalare per %s" % url)
        return "loopback"
    a = res["nets"]
    emails = []
    definitive = ""
    for x in a:
        if(x["emails"]!="None"):
            emails.append(x["emails"])
    for k in emails:
        try:
            for j in k:
                definitive+=j+";"
        except Exception as err:
            return;
    return list(set(definitive[:-1].split(";")))

def signal():
    while not queue_url.empty():
        x = queue_url.get()
        x=x.replace("\n","")
        e = getEmails(x)
        if(str(e)=="loopback" or str(e)=="None" ):
            with open(error_sign, "a") as myfile:
                if(str(e)=="None"):
                    myfile.write(x+" ==> PROBLEMA: Indirizzo mail non trovato SOLUZIONE: Prova qui https://centralops.net/co/\n")
                elif (str(e)=="loopback"):
                    myfile.write(x+" ==> PROBLEMA: Loopback SOLUZIONE: Può capitare per dominio già abbattuto\n")
            continue;
        else:
            for j in (e):
                sendMail(j,x)
            print("[OK] ==> Segnalazione effettuata per",x)
            with open(already_sign, "a") as myfile:
                myfile.write(x+"\n")

print("Eseguo task")
avvio()
if (os.path.exists("File.txt")):
    os.remove("File.txt")
if (not os.path.exists(already_sign)):
    check = False
saveFile()
print("Pulizia possibili valori duplicati in corso...")
f = filetolist("File.txt")
print("Sono state caricate in totale %s righe (duplicati non presenti). Verranno segnalate effettivamente: " % len(f),end="")
for x in f:
    if(not isvalid(x)):
        continue
    if(check):
        if(not already(x)):
            queue_url.put(x)
    else:
        queue_url.put(x)
if(queue_url.qsize() == len(f)):
    print(str(queue_url.qsize())+" url")
else:
    print(str(queue_url.qsize())+" url (tolte "+str(len(f)-queue_url.qsize())+" righe tra host non validi e url già segnalate)")
time.sleep(5)
for t in range(thread):
    th = threading.Thread(target=signal())
    th.start()
while not queue_url.empty():
    continue
fine()
