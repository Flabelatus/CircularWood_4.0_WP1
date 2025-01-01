# FTP to help Transfering the CAM files to the Robot controller
import os
import io
import re
from time import sleep
from typing import List

from ftplib import FTP

from workflow.api_http_client.api_client import http_client
from workflow.production_run import ProductionCore, logger
from workflow.production_run.rapid_parser import RAPIDParser


class RapidTransferLink(FTP, ProductionCore):
    """
    Handles transferring RAPID code files to the robot controller via FTP.
    """

    def __init__(self):
        """
        Initialize the FTP client and connect to the server.

        """
        FTP.__init__(self)
        ProductionCore.__init__(self)

        self.root_dir = self.params.root_dir
        self.robo_ftp_conf = self.params.ftp
        self.ip = self.robo_ftp_conf.ip
        self.username = self.robo_ftp_conf.credentials.get('username')
        self.password = self.robo_ftp_conf.credentials.get('password')
        self.target_directory = self.robo_ftp_conf.directory
        self.connect(host=self.ip)
        self.login(user=self.username, passwd=self.password)

    def upload_file(self, input_path: str, target_directory: str, target_path: str):
        """
        Upload a file to the FTP server.

        Args:
            input_path (str): Local file path to upload.
            target_directory (str): Remote directory on the FTP server.
            target_path (str): Full target path (including filename) on the server.
        """
        try:
            with open(input_path, 'r') as file:
                rapid_code = file.read()

            rapid_file_stream = io.BytesIO(rapid_code.encode('ascii'))

            try:
                self.mkd(target_directory)
            except Exception as e:
                logger.warning(f"Directory creation failed or already exists: {e}")

            self.cwd(target_directory)
            self.storbinary(f'STOR {target_path}', rapid_file_stream)

            # Verify file upload
            local_file_size = len(rapid_code)
            remote_file_size = self.size(target_path)
            if local_file_size == remote_file_size:
                logger.info(f"File {input_path} uploaded successfully with correct size.")
            else:
                logger.error(f"File size mismatch! Local: {local_file_size}, Remote: {remote_file_size}")
        except Exception as e:
            logger.error(f"Failed to upload file {input_path}: {e}")

    @staticmethod
    def fetch_rapid_from_db(wood_id: int) -> List[dict]:
        """
        Fetch RAPID code from the database based on a wood ID.

        Args:
            wood_id (int): The wood ID.

        Returns:
            List[dict]: A list of RAPID code instructions as dictionaries.
        """
        try:
            return [{prod.get('id'): prod.get('instruction')} for prod in http_client.fetch_production_by_wood_id(wood_id)]
        except Exception as e:
            logger.error(f"Failed to fetch RAPID code for wood ID {wood_id}: {e}")
            return []

    def transfer_rapid_code(self, wood_id: int, msg):
        """
        Fetch, parse, and upload RAPID code to the FTP server.

        Args:
            wood_id (int): The wood ID for fetching RAPID code.
            target_directory (str): Target directory on the FTP server.
        """
        try:
            rapid_codes = self.fetch_rapid_from_db(wood_id)
            if not rapid_codes:
                logger.error("No RAPID code fetched from the database.")
                return

            for content in rapid_codes:
                try:
                    logger.info(f"topic {msg.topic}", str(msg.payload.decode()[2:]))

                    # Use RapidParser to parse the content
                    parser = RAPIDParser(content.get('instructions'))
                    part_side_1, part_side_2 = parser.split_rapid()
                    
                    # Generate filenames
                    side_1_filename = f"{wood_id}_{content.get('id')}_side_1.mod"
                    side_2_filename = f"{wood_id}_{content.get('id')}_side_2.mod"
                    
                    # For testing only
                    with open(os.path.join(self.root, 'scripts', 'example_RAPID', side_1_filename), 'w') as mod_file:
                        mod_file.write(part_side_1)

                    with open(os.path.join(self.root, 'scripts', 'example_RAPID', side_2_filename), 'w') as mod_file:
                        mod_file.write(part_side_2)

                    # Upload parsed parts
                    self.upload_file(part_side_1, self.target_directory, side_1_filename)
                    self.upload_file(part_side_2, self.target_directory, side_2_filename)

                    sleep(0.5)
                    logger.debug("Files uploaded")

                except Exception as e:
                    logger.error(f"Error parsing or uploading RAPID code: {e}")
        except Exception as e:
            logger.error(f"Error during RAPID code transfer: {e}")