import smtplib
sender = 'extrlus.options-it.com'
receivers = 'jujjavarapumahesh98@gmail.com'
message = """From: 'noreply@ihsmarkit.com'
To: 'jujjavarapumahesh98@gmail.com'
Subject: SMTP e-mail test
This is a test e-mail message.
"""
smtpObj = smtplib.SMTP('extrlus.options-it.com',25)
smtpObj.sendmail(sender, receivers, message)         
print("Successfully sent email")
 