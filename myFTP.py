#!/usr/bin/env python

## myFTP Module is written by Jason/Ge Wu 
## Default FTP port:21 Pass the file path and name to the function!

import ftplib
import os
import time

host = ""       ## User your FTP Server Address
username = ""      ## User your FTP Server Username
password = ""  ## User your FTP Server Password
default_port = 21

def FTP_upload(filename_local,filepath_server):
    ## filename_local: The file name and the directory on local
    ## filepath_server: The directory of FTP server. Home directory just pass blank
    ftp = ftplib.FTP()
##    ftp.set_debuglevel(2)
    ftp.connect(host,default_port)
    ftp.login(username,password)
    print ftp.getwelcome()
    if (os.path.isfile(filename_local)):
        try:
            ftp.cwd(filepath_server)
            file_buffer = open(filename_local,'rb')
            ftp.storbinary("STOR %s" % os.path.basename(filename_local), file_buffer, 1024)
##            ftp.set_debuglevel(0)    
            file_buffer.close()
            ftp.quit()
            print "Upload Succeed! "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            return True
        except:
            print "Upload Failed! "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            file_buffer.close()
            return False
    else:
        print "Please check the file path..."
        return False

def FTP_download(filename_local,filename_server,filepath_server):
    ## filename_local: The file name and the directory on local
    ## filename_server: The file name in the correct directory of FTP server
    ## filepath_server: The directory of FTP server. Home directory just pass blank
    ftp = ftplib.FTP()
##    ftp.set_debuglevel(2)
    ftp.connect(host,default_port)
    ftp.login(username,password)
    print ftp.getwelcome()
    try:
        ftp.cwd(filepath_server)
        file_buffer = open(filename_local, 'wb').write
        ftp.retrbinary("RETR %s" % os.path.basename(filename_server), file_buffer, 1024)
##        ftp.set_debuglevel(0)
##        file_buffer.close()
        ftp.quit()
        print "Download Succeed! "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return True
    except:
        print "Download Failed! "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return False


## Common the "main" below when you are using this module
##if __name__ == "__main__":
##    filename = "/home/pi/Image/123 321.jpg"
##    filepath = ""
##    FTP_upload(filename,"/Image")
