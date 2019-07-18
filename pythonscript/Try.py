#!/usr/bin/python
import smtplib 
from smtplib import SMTP


import socket 


sender = 'noreply@ihsmarkit.com'
receivers = ['mahesh.jujjavarapu@ihsmarkit.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <mahesh.jujjavarapu@ihsmarkit.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""   


smtpObj = smtplib.SMTP( 'extrlus.options-it.com':25  )



smtpObj.sendmail(sender, receivers, message)         
print ("Successfully sent email")