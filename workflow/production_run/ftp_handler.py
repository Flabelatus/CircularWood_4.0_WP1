# FTP to help Transfering the CAM files to the Robot controller
import io
from time import sleep
import requests
from ftplib import FTP

class RAPID_FTP:
    def __init__(self, ip, user, passwd):
        """
        Initializes the FTP client with the provided IP address, username, and password.

        Args:
            ip (str): The IP address of the FTP server.
            user (str): The username for the FTP connection.
            passwd (str): The password for the FTP connection.
        """
        self.ip = ip
        self.FTP_user = user
        self.FTP_password = passwd

    def upload_file(self,inputPath,targetDirectory, targetPath):
        """
        Uploads a file to the specified target path on the FTP server.

        Args:
            inputPath (str): The path to the file to upload on the local machine.
            targetDirectory (str): The directory on the FTP server to upload the file to.
            targetPath (str): The target path (including filename) on the FTP server for the uploaded file.
        """
        with open(inputPath, 'r') as file:
            RAPID_code = file.read()
        instant_rapid_file_1 = io.BytesIO(bytes(RAPID_code, 'ascii'))

        with FTP(host=self.ip, user=self.FTP_user, passwd=self.FTP_password) as ftp:
            try:
                ftp.mkd(targetDirectory)
            except Exception as e:
                print(f"Directory creation failed or already exists: {e}")

            ftp.cwd(targetDirectory)
            ftp.storbinary(f'STOR {targetPath}', instant_rapid_file_1)

            sleep(1)

            # verify file with a "sort of checksum"
            local_file_size = len(RAPID_code)
            remote_file_size = ftp.size(targetPath)
            if local_file_size == remote_file_size:
                print(f"File {inputPath} uploaded with correct size")
            else:
                print(f"File size mismatch! Local: {local_file_size}, Remote: {remote_file_size}")

    def write_string_to_file(self,step_data, filename):
        """
        Writes a string to a file.

        Args:
            step_data (str): The data to be written to the file.
            filename (str): The name of the file to write to.
        """
        with open(filename, 'w') as step_file:
            step_file.write(step_data)

    #TODO endpoint and json array index stil needs to be updated to correct file
    #TODO endpoint and json array index stil needs to be updated to correct file
    #TODO endpoint and json array index stil needs to be updated to correct file
    def fetch_rapid_from_db(self,wood_id, PartNr, ClampLocation):
        response = requests.get(f"https://robotlab-residualwood-dev.onrender.com/production/wood/{wood_id}")
        # print(response.json())
        if response.status_code == 200:
            instruction = response.json()[-1].get('instruction')
            return instruction

    #TODO endpoint and json array index stil needs to be updated to correct file
    #TODO endpoint and json array index stil needs to be updated to correct file
    #TODO endpoint and json array index stil needs to be updated to correct file

    def GetRAPID_Multiples(self,WoodID, partnr=1, clamp=1):
        """
        Fetches RAPID code from a database using a provided wood ID.

        **NOTE:** This function requires further implementation to update the endpoint and
                 handle the JSON array index correctly.

        Args:
            wood_id (str): The ID of the wood to retrieve RAPID code for.
            PartNr (int): The part number (potentially unused).
            ClampLocation (int): The clamp location (potentially unused).

        Returns:
            str: The RAPID code retrieved from the database (if successful).
        """
        file = self.fetch_rapid_from_db(str(WoodID), partnr, clamp)
        self.write_string_to_file(file, "temp.modx")
        # print("instruction field = ", file)

        with open('temp.modx', 'w') as fileLocation:
            fileLocation.write(file)
        return file

    def RAPID_FTP_main(self,WoodID, msg, rapid_File_Path_1, rapid_File_Path_2, Inbetween_RAPID_Marker, targetDirectory):
        """
        Fetches, splits, and uploads RAPID code to an FTP server.

        Args:
            WoodID (str): The ID of the wood to retrieve RAPID code for.
            msg (Message): MQTT message object.
            rapid_File_Path_1 (str): The target path for the first part of the RAPID code on the FTP server.
            rapid_File_Path_2 (str): The target path for the second part of the RAPID code on the FTP server.
            Inbetween_RAPID_Marker (str): A marker used to split the RAPID code into two parts.
            targetDirectory (str): The target directory on the FTP server for the uploaded files.
        """
        RAPID_string = self.GetRAPID_Multiples(WoodID=WoodID)
        print("rapid string fetched")

        file_part1, file_part2 = RAPID_string.split(Inbetween_RAPID_Marker)
        print("rapid string split")

        # Write the contents to two separate files
        with open('../../scripts/example_RAPID/Example.mod', 'w') as part1_file:
            part1_file.write(file_part1)
        print("1st saved as mod")

        with open('../../scripts/example_RAPID/Reversed.mod', 'w') as part2_file:
            part2_file.write(file_part2)
        print("2nd saved as mod")

        try:
            print(f"topic {msg.topic}", str(msg.payload.decode()[2:]))
            #partNr = int(msg.payload.decode()[2:])
            #print("partNr = ", partNr, "  Clamp =", msg.topic)

            file_path_Normal = '../../scripts/example_RAPID/Example.mod'
            file_path_Reversed = '../../scripts/example_RAPID/Reversed.mod'

            print("starting uploading RAPID")
            self.upload_file(file_path_Normal, targetPath=rapid_File_Path_1,targetDirectory = targetDirectory)
            print("1st code uploaded")
            self.upload_file(file_path_Reversed, targetPath=rapid_File_Path_2,targetDirectory = targetDirectory)
            print("2nd code uploaded")
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!
            sleep(1)
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!
            # REMOVE THIS LINE LATER, THIS LINE IS FOR TESTING PURPOSES!!!!!!!!!!!!!!!!!

            print("uploading done")

        except Exception as e:
            print("Something went wrong :", e)
