import subprocess
import time
import datetime

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

date = str(datetime.datetime.now())
d=date.split()
filename = "RC-"+d[0]+".txt"

def mail1(fname):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('email', 'password') # Sender eamil and password
    toaddr = cc = ['receiver 1 mail','receiver 2 mail','receiver 3 mail']
    cc = ['receiver 2 mail','receiver 3 mail']
    msg = MIMEMultipart()
    msg['From'] = 'ZZZZ'
    msg['to'] = 'receiver 1 mail'
    msg['Cc'] = ','.join(cc)
    msg['Subject'] = 'Report'

    message = """
    Report of ....
    .......
    .......
    """

    msg.attach(MIMEText(message, 'plain'))

    filename = fname
    attachment = open(filename, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(p)

    text = msg.as_string()
    server.sendmail('Connectivity TEST', toaddr, text)
    server.quit()



ip_table = {
    "Device 1" : "ip add of Device 1",
    "Device 2" : "ip add of Device 2",
    "Device 3" : "ip add of Device 3"
}

r = open(filename, 'a')
newip = ''

def ping(ip):
    ping_reply = subprocess.run(["ping","-c2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE) # "-c2" is of Linux, use "-n","2" for Windows
    result =""
    if ping_reply.returncode == 0:      #ping will return 0 => success or  1 => Fail
        if ("unreachable" in str(ping_reply.stdout)):
            result = ("\n*  %s DOWN ===> OFFLINE  " % ip)
        else:
            result= ("\n* %s UP  ===> ONLINE  " % ip)
    elif ping_reply.returncode == 1:
        result= ("\n*  %s DOWN ===> OFFLINE  " % ip)
    return result


def add():
    global r
    global newip
    r.write(newip)

def generator(date,r):
    r.write(f"Report du {date} \n")
    r.write(" \n")
    for name, ip in ip_table.items():
        print(name, end=' ')
        print(ping(ip))
        print("----")
        r.write(name)
        r.write(ping(ip) + '\n')
        r.write("----" + '\n')

    r.close()

for l in ip_table:
    print(l+' : '+ ip_table[l])

generator(date,r)
mail1(filename)
