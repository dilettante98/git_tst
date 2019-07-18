# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
 

me= 'extrlus.options-it.com'
you='jujjavarapumahesh98@gmail.com'
msg['Subject'] = 'error occured'
msg['From'] = 'noreply@ihsmarkit.com'
msg['To'] = 'mahesh.jujjavarapu@ihsmarkit.com'


s = smtplib.SMTP('extrlus.options-it.com',25)
s.sendmail(me, [you], msg.as_string())
s.quit()