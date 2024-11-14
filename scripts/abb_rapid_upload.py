import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.production_run import ftp_handler
from settings import WorkflowManagerConfig

if __name__ == '__main__':
    ftp_params = WorkflowManagerConfig().get_ftp_params()

    ip = ftp_params["RED"]['ip']
    user = ftp_params["RED"]['username']
    passwd = ftp_params["RED"]['password']

    rapid_ftp = ftp_handler.RAPID_FTP(ip=ip, user=user, passwd=passwd)
    rapid_ftp.upload_file(inputPath="example_RAPID/Example.mod", targetDirectory="MILLING_UPLOAD",
                          targetPath="Example.mod")