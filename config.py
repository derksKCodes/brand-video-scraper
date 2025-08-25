import os
from dotenv import load_dotenv

load_dotenv()

# Brand keywords
BRAND_KEYWORDS = os.getenv("BRAND_KEYWORDS", "Ancient Bliss")

# Google Drive
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

# Google Drive root folder for uploads
DRIVE_ROOT_FOLDER_ID = os.getenv("DRIVE_ROOT_FOLDER_ID", "your-folder-id")
