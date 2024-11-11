# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#TODO imports

if __name__ == '__main__':
    rapid_ftp = RAPID_FTP(ip='10.0.0.14', user='Default User', passwd='robotics')
    rapid_ftp.upload_file(inputPath="Fetched_RAPID/Normal.mod", targetDirectory="MILLING_UPLOAD",
                          targetPath="Normal.mod")
