from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GoogleDriveUploader:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile("/client_secrets.json")
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)
        self.folder_ids = {}

    
    def upload(self, local_path, drive_filename):
        # Create the file object with the specific title you want
        file_drive = self.drive.CreateFile({'title': drive_filename})
        file_drive.SetContentFile(local_path)
        file_drive.Upload()
        print(f"Uploaded {drive_filename} to Google Drive root.")