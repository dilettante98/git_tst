from smtplib import SMTPException
import smtplib

sender = '123@gmail.com'
receivers = 'mahesh.zomato98@gmail.com'

message = """From: From Person <123@gmail.com>
To: To Person <mahesh.zomato98@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('extrlus.options-it.com', 25)
   smtpObj.sendmail(sender, receivers, message)         
   print ("Successfully sent email")
except SMTPException:
   print( "Error: unable to send email")