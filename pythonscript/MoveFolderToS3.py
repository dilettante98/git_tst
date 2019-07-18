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


# For Debug
start_date = '2019-01-02'
end_date = '2019-01-02'
fromPath = "z:\equities"
bucketName = "testingmovetobucket"
bucketFolder = "Activ_Raw_MD"
newIntervalPath = "y:\equities"

# if (arguments < position):  
#     print ("Please provide arguments in following format:\nstartdate:<YYYY-MM-DD> enddate:<YYYY-MM-DD>  REGpath: bucketname: bucketfolder: TAGpath:\nNote:path need not to put with any quotes.")
# else:
#     start_date= sys.argv[1]
#     end_date=sys.argv[2]
#     fromPath = sys.argv[3]
#     bucketName=sys.argv[4]
#     bucketFolder=sys.argv[5]
#     newIntervalPath=sys.argv[6]

fromPath=fromPath.replace("/", "\\")
newIntervalPath=newIntervalPath.replace("/", "\\")

s_date = datetime.strptime(start_date, '%Y-%m-%d')
e_Date = datetime.strptime(end_date, '%Y-%m-%d')


#logger
logfile = 'C:\logs\S3_Utility_Script2_' +  datetime.now().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(filename= logfile, level=logging.INFO, format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s')



 

def get_content_md5(filepath):
    try :
        content = read_file_as_binary(filepath)
        digest = hashlib.md5(content).digest()
        return base64.b64encode(digest).decode("utf8")
    except Exception as e:
        logging.info("Error %s occured." % e)
        

def read_file_as_binary(filepath):
    with open(filepath,'rb') as f:
        return f.read()

def iterateViaDirectory( path,dir,bucketName,bucketFolder):
    if datetime.strptime(dir, '%Y-%m-%d') >= s_date and datetime.strptime(dir, '%Y-%m-%d') <= e_Date:
                dir_path = os.path.join(path, dir)                                                   
                logging.info("Directory created : " + dir_path)
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                     try :
                        cur_md5 = get_content_md5(os.path.join(root,file))
                        tempfilepath=os.path.join(root,file)
                        datacontent = read_file_as_binary(tempfilepath)
                        s3C.put_object(Body=datacontent, Bucket=bucketName, Key=bucketFolder+"/"+dir + "/" +file, ContentMD5='gjxgf'+cur_md5) 
                        
                        logging.info("File uploaded : %s ", os.path.join(root,file))
                     except Exception as e:
                            logging.info('Error: %s' % e)
                            

def uploadDirectory(path, bucketName,bucketFolder):    
    for root,dirs,files in os.walk(path):        
        for dir in dirs:            
            iterateViaDirectory(path,dir,bucketName,bucketFolder)

uploadDirectory(fromPath,bucketName,bucketFolder)


print("Uploaded to s3")