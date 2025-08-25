# video_scraper_project/uploader/drive_uploader.py

import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from config import DRIVE_FOLDER_BASE, DRIVE_CREDENTIALS_FILE, DRIVE_TOKEN_FILE

class DriveUploader:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = None
        self.folder_ids = {}  # Cache for folder IDs
        
        # Set settings for OAuth
        self.gauth.settings['client_config_file'] = DRIVE_CREDENTIALS_FILE
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive"""
        try:
            # Try to load saved credentials
            self.gauth.LoadCredentialsFile(DRIVE_TOKEN_FILE)
            
            if self.gauth.credentials is None:
                # Authenticate if no credentials available
                self.gauth.LocalWebserverAuth()
            elif self.gauth.access_token_expired:
                # Refresh if expired
                self.gauth.Refresh()
            else:
                # Initialize with saved credentials
                self.gauth.Authorize()
                
            # Save credentials
            self.gauth.SaveCredentialsFile(DRIVE_TOKEN_FILE)
            
            # Use offline mode to get a refresh token
            self.gauth.LocalWebserverAuth(access_type='offline', prompt='consent')
            
            # Create drive instance
            self.drive = GoogleDrive(self.gauth)
            
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    
    def get_or_create_folder(self, folder_name, parent_id=None):
        """Get or create a folder in Google Drive"""
        # Check if we already have the folder ID cached
        if folder_name in self.folder_ids:
            return self.folder_ids[folder_name]
        
        # Query for existing folder
        query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        folder_list = self.drive.ListFile({'q': query}).GetList()
        
        if folder_list:
            folder_id = folder_list[0]['id']
        else:
            # Create new folder
            folder_metadata = {
                'title': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                folder_metadata['parents'] = [{'id': parent_id}]
                
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']
        
        # Cache the folder ID
        self.folder_ids[folder_name] = folder_id
        return folder_id
    
    def upload_file(self, file_path, platform_name):
        """Upload a file to Google Drive in the appropriate folder structure"""
        try:
            # Get or create base folder
            base_folder_id = self.get_or_create_folder(DRIVE_FOLDER_BASE)
            
            # Get or create platform folder
            platform_folder_id = self.get_or_create_folder(platform_name, base_folder_id)
            
            # Create file metadata
            file_name = os.path.basename(file_path)
            file_metadata = {
                'title': file_name,
                'parents': [{'id': platform_folder_id}]
            }
            
            # Create and upload file
            file_drive = self.drive.CreateFile(file_metadata)
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            
            return file_drive['id']
            
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None