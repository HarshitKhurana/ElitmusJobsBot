#!/usr/bin/python

# Harshit Khurana
# 08.01.18

import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "user@gmail.com"
gmail_pwd = "user@password"

def login(user):
   global gmail_user, gmail_pwd
   gmail_user = user
   gmail_pwd = getpass.getpass('\n\n**********\n[*] Password for %s: ' % gmail_user)

def mailto(to, subject, text, attachment):
   message = MIMEMultipart()
   message['From'] = gmail_user
   message['To'] = to
   message['Subject'] = subject
   message.attach(MIMEText(text))

   if attachment:
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(open(attachment, 'rb').read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
      message.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, message.as_string())
   mailServer.close()
   os.system("rm -f Elitmus-Jobs.txt")

def example_elitmus(email , recepient , subject , content , attachment):

   login(email)
   mailto(recepient , subject , content , attachment)

