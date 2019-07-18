import smtplib
import os
import boto3
import sys
import getopt
import logging
import shutil
import base64
import hashlib
import pathlib
from os import walk
from datetime import datetime, timedelta

s3C = boto3.client('s3')
start_date = ''
end_date = ''
fromPath = ""
bucketName = ""
bucketFolder = ""
position = 5
arguments = len(sys.argv) - 1
logfile = ''

#For Debug
start_date = '2019-01-02'
end_date = '2019-01-02'
fromPath = "z:\equities\\2019-01-02"
bucketName = "testingmovetobucket"
bucketFolder = "Activ_Raw_MD"

# if (arguments < position):
#     print("Please provide arguments in following format:\nstartdate:<YYYY-MM-DD> enddate:<YYYY-MM-DD>  REGpath: bucketname: bucketfolder:  \nNote:path need not to put with any quotes.")
# else:
#     start_date = sys.argv[1]
#     end_date = sys.argv[2]
#     fromPath = sys.argv[3]
#     bucketName = sys.argv[4]
#     bucketFolder = sys.argv[5]


fromPath = fromPath.replace("/", "\\")
bucketFolder = bucketFolder.replace("\\", "/")
s_date = datetime.strptime(start_date, '%Y-%m-%d')
e_Date = datetime.strptime(end_date, '%Y-%m-%d')
# logger
logfile = 'C:\logs\S3_Utility2_' + datetime.now().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(filename=logfile, level=logging.INFO,
                    format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s')


def get_content_md5(filepath):
    try:
        content = read_file_as_binary(filepath)
        digest = hashlib.md5(content).digest()
        return base64.b64encode(digest).decode("utf8")
    except Exception as e:
        logging.info("Error %s occured." % e)


def read_file_as_binary(filepath):
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except Exception as e:
        logging.info("Error %s occured." % e)


def mail_notification(Exception):
 try:
    sender = 'testingdates@ihsmarkit.com'
    receivers = ['mahesh.jujjavarapu@ihsmarkit.com']
    message = """From: From Person <testingdates@ihsmarkit.com>
    To: To Person <mahesh.jujjavarapu@ihsmarkit.com>
    Subject: Error occured during file upload to S3
    Error occured during the file upload to s3 and these are the details: {} 
    """.format(Exception)
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
    print ("Successfully sent email")
 except Exception as e:
    print ("Error: unable to send email %s",e)



def validate_file_for_copy(file, temp_location, bucketName, bucketFolder):
    try:
        day_count = (e_Date - s_date).days + 1
        for single_date in [d for d in (s_date + timedelta(n) for n in range(day_count)) if d <= e_Date]:
            date_in_string = single_date.strftime("%Y-%m-%d")
            dateinstring = date_in_string.replace("-", "")
            if date_in_string in file or dateinstring in file:
                filepath_is = os.path.join(temp_location, file)
                cur_md5 = get_content_md5(filepath_is)
                datacontent = read_file_as_binary(filepath_is)
                s3C.put_object(Body=datacontent, Bucket=bucketName,
                               Key=bucketFolder+"/" + file, ContentMD5="j"+cur_md5)
                logging.info("File uploaded : %s ", filepath_is)
    except Exception as e:
        logging.info('Error: %s' % e)
        mail_notification(e)


def uploadDirectory(fromPath, bucketName, bucketFolder):
    for file in os.listdir(fromPath):
        if file.endswith('.txt') or file.endswith('.gz'):
            validate_file_for_copy(file, fromPath, bucketName, bucketFolder)


uploadDirectory(fromPath, bucketName, bucketFolder)
print("Uploaded to s3")
