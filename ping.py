import subprocess
import datetime
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

date = str(datetime.datetime.now())
d=date.split()
filename = "RC-"+d[0]+".txt"
ip_table = {
    "localhost" : "127.0.0.1",
}
r = open(filename, 'a')
newip = ''


def mail1(fname):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('sender_email', 'password***')
    msg = MIMEMultipart()
    msg['From'] = 'IT'
    msg['to'] = 'receiver_email'
    msg['Subject'] = 'Object'
    message = """
    Test
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
    server.sendmail('sender_email', 'receiver_email', text)
    server.quit()


def mail2():
    gmail_user = 'sender_email'
    gmail_password = 'password***'
    sent_from = gmail_user
    to = ['receiver_email']
    subject = 'OMG Super Important Message'
    body = "Hey, what's up?\n\n - You"
    email_text = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')


def ping(ip):
    ping_reply = subprocess.run(["ping","-n","2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    result =""
    if ping_reply.returncode == 0:      # ping will return 0 => success or  1 => Fail
        if ("unreachable" in str(ping_reply.stdout)):
            result = ("\n*  %s Don't Respond ===> OFFLINE  " % ip)
        else:
            result= ("\n* %s Respond ===> ONLINE  " % ip)
    elif ping_reply.returncode == 1:
        result= ("\n*  %s Don't Respond ===> OFFLINE  " % ip)
    return result


def generator(date,r):
    r.write(f"Connectivity report of Key equipment (Local and Remote) of the {date} \n")
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

ans = input('Do you want to modify the list ? Y/N : \n => ')
ans = ans.lower()

if ans == "n":
    generator(date,r)
    mail1(filename)
elif ans == 'y':
    an = input("""
    1- Add
    2- Modify  \n => 
    """)

    if an == "1":
        cc = True
        while cc:
            nam = input("Equipment name : \n => ")
            ip = input("IP adress: : \n => ")
            ip_table[nam] = ip
            cho1 = input('Do you want to make another change ? Y/N : \n => ')
            cho1 = cho1.lower()
            if cho1 == 'y':
                cc = True
            elif cho1 == 'n':
                cc = False
                break
            else:
                break
    elif an == "2":
        choice = input("""
        Do you want to change ?
        1- Name and IP
        2- Name
        3- IP : \n => """)
        choice = choice.lower()
        if choice == "1":
            c = True
            while c:
                nam = input("Name of the equipment to modify : \n =>  ")
                if nam in ip_table.values():
                    nnam = input("New Equipment Name : \n => ")
                    nip = input("New IP address : \n => ")
                    ip_table[nnam] = ip_table.pop(nam)
                    ip_table[nnam] = nip
                    cho = input('Do you want to make another change ? Y/N : \n => ')
                    cho = cho.lower()
                    if cho == 'y':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
                else:
                    print("Wrong entry")
                    cho = input('Do you want to make another change ? Y/N : \n => ')
                    cho = cho.lower()
                    if cho == 'y':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
            generator(date, r)
        if choice == "2":
            c = True
            while c:
                nam = input("Name of the equipment to modify : \n => ")
                if nam in ip_table.values():
                    nnam = input("New Equipment Name : \n => ")
                    ip_table[nnam] = ip_table.pop(nam)
                    cho = input('Do you want to make another change ? Y/N : \n => ')
                    cho = cho.lower()
                    if cho == 'y':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
                else:
                    print("Wrong entry")
                    cho = input('Do you want to make another change ? Y/N : \n => ')
                    cho = cho.lower()
                    if cho == 'y':
                        c = True
                    elif cho == 'n':
                        c = False
                        break
                    else:
                        break
                generator(date, r)
            if choice == "3":
                c = True
                while c:
                    nam = input("Name of the equipment to modify : \n => ")
                    if nam in ip_table.values():
                        nip = input("New IP address : \n => ")
                        ip_table[nnam] = nip
                        cho = input('Do you want to make another change ? Y/N : \n => ')
                        cho = cho.lower()
                        if cho == 'y':
                            c = True
                        elif cho == 'n':
                            c = False
                            break
                        else:
                            break
                    else:
                        print("Wrong entry")
                        cho = input('Do you want to make another change ? Y/N : \n => ')
                        cho = cho.lower()
                        if cho == 'y':
                            c = True
                        elif cho == 'n':
                            c = False
                            break
                        else:
                            break
                    generator(date, r)
    generator(date, r)
    mail1(filename)
