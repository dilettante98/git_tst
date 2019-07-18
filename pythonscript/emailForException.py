import smtplib
sender = 'noreply@ihsmarkit.com'
receivers = ['mahesh.jujjavarapu@ihsmarkit.com']
message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test
This is a test e-mail message.
"""
 
smtpObj = smtplib.SMTP_SSL('extrlus.options-it.com')
smtpObj.sendmail(sender, receivers, message)         
print ("Successfully sent email")
