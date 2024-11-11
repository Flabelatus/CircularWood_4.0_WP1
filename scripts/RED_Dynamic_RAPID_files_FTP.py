import io
from time import sleep
import requests
from ftplib import FTP

class RAPID_FTP:
    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.FTP_user = user
        self.FTP_password = passwd

    def upload_file(self,inputPath,targetDirectory, targetPath):
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
        with open(filename, 'w') as step_file:
            step_file.write(step_data)

    def fetch_rapid_from_db(self,wood_id, PartNr, ClampLocation):
        response = requests.get(f"https://robotlab-residualwood-dev.onrender.com/production/wood/{wood_id}")
        # print(response.json())
        if response.status_code == 200:
            instruction = response.json()[-1].get('instruction')
            return instruction

    def GetRAPID_Multiples(self,WoodID, partnr=1, clamp=1):
        file = self.fetch_rapid_from_db(str(WoodID), partnr, clamp)
        self.write_string_to_file(file, "temp.modx")
        # print("instruction field = ", file)

        with open('temp.modx', 'w') as fileLocation:
            fileLocation.write(file)
        return file

    def RAPID_FTP_main(self,WoodID, msg, rapid_File_Path_1, rapid_File_Path_2, Inbetween_RAPID_Marker, targetDirectory):
        RAPID_string = self.GetRAPID_Multiples(WoodID=WoodID)
        "rapid string fetched"

        file_part1, file_part2 = RAPID_string.split(Inbetween_RAPID_Marker)
        print("rapid string split")

        # Write the contents to two separate files
        with open('Fetched_RAPID/Normal.mod', 'w') as part1_file:
            part1_file.write(file_part1)
        print("normal saved as mod")

        with open('Fetched_RAPID/Reversed.mod', 'w') as part2_file:
            part2_file.write(file_part2)
        print("reversed saved as mod")

        try:
            print(f"topic {msg.topic}", str(msg.payload.decode()[2:]))
            #partNr = int(msg.payload.decode()[2:])
            #print("partNr = ", partNr, "  Clamp =", msg.topic)

            file_path_Normal = 'Fetched_RAPID/Normal.mod'
            file_path_Reversed = 'Fetched_RAPID/Reversed.mod'

            print("starting uploading RAPID")
            self.upload_file(file_path_Normal, targetPath=rapid_File_Path_1,targetDirectory = targetDirectory)
            print("normal code uploaded")
            self.upload_file(file_path_Reversed, targetPath=rapid_File_Path_2,targetDirectory = targetDirectory)
            print("Reversed code uploaded")
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
