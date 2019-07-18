import os,boto3,sys,getopt,logging,shutil,base64, hashlib, pathlib
from os import walk
from datetime import datetime, timedelta

s3C = boto3.client('s3')
start_date = ''
end_date = ''
fromPath = ""
bucketName = ""
bucketFolder = ""
newIntervalPath = ""
position=6
arguments = len(sys.argv) - 1
logfile = ''

# #For Debug
# start_date = '2019-01-02'
# end_date = '2019-01-02'
# fromPath = "z:\equities"
# bucketName = "testingmovetobucket"
# bucketFolder = "Activ_Raw_MD"
# newIntervalPath = "y:\equities"


if (arguments < position):  
    print ("Please provide arguments in following format:\nstartdate:<YYYY-MM-DD> enddate:<YYYY-MM-DD>  REGpath: bucketname: bucketfolder: TAGpath:\nNote:path need not to put with any quotes.")
else:
    start_date= sys.argv[1]
    end_date=sys.argv[2]
    fromPath = sys.argv[3]
    bucketName=sys.argv[4]
    bucketFolder=sys.argv[5]
    newIntervalPath=sys.argv[6]

frompath=fromPath.replace("/", "\\")
newIntervalPath=newIntervalPath.replace("/", "\\")

s_date = datetime.strptime(start_date, '%Y-%m-%d')
e_Date = datetime.strptime(end_date, '%Y-%m-%d')
#logger
logfile = 'C:\logs\S3_Utility_' +  datetime.now().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(filename= logfile, level=logging.INFO, format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s')

def syncFiles(src,fdate,dest):
    try:
        for filename in os.listdir(src):
         if fdate in filename:
            temp_location=os.path.join(newIntervalPath, filename)
            locationAtDestination=os.path.join(dest,filename)
            if not os.path.exists(locationAtDestination):
                os.system ("copy /y " + temp_location + " " + dest)
                logging.info("copied file from %s to %s",temp_location ,dest)
            else:
                logging.info(" %s file already exists in the location ",temp_location)
    # Directories are the same
    except os.error as e:
        logging.info("Directory not copied. Error: %s" % e)
    # Any error saying that the directory doesn't exist

def get_content_md5(filepath):
    try :
        content = read_file_as_binary(filepath)
        digest = hashlib.md5(content).digest()
        return base64.b64encode(digest).decode("utf8")
    except Exception as e:
        logging.info("Error %s occured.",Exception)
        

def read_file_as_binary(filepath):
    with open(filepath,'rb') as f:
        return f.read()

def iterateViaDirectory( path,dir,bucketName,bucketFolder):
    if datetime.strptime(dir, '%Y-%m-%d') >= s_date and datetime.strptime(dir, '%Y-%m-%d') <= e_Date:
                dir_path = os.path.join(path, dir)                                                   
                syncFiles(newIntervalPath, dir,dir_path)                  
                logging.info("Directory created : " + dir_path)
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                     try :
                        cur_md5 = get_content_md5(os.path.join(root,file))
                        tempfilepath=os.path.join(root,file)
                        datacontent = read_file_as_binary(tempfilepath)
                        s3C.put_object(Body=datacontent, Bucket=bucketName, Key=bucketFolder+"/"+dir + "/" +file, ContentMD5=cur_md5) 
                        
                        logging.info("File uploaded : %s ", os.path.join(root,file))
                     except Exception as e:
                            logging.info('Error: %s' % e)
                            


		

def uploadDirectory(path, bucketName,bucketFolder):    
    for root,dirs,files in os.walk(path):        
        for dir in dirs:            
            iterateViaDirectory(path,dir,bucketName,bucketFolder)



uploadDirectory(frompath,bucketName,bucketFolder)


print("Uploaded to s3")