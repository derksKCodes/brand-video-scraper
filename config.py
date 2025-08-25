import os
from dotenv import load_dotenv

load_dotenv()

# video_scraper_project/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Brand configuration
BRAND_NAME = "Ancient Bliss"
BRAND_KEYWORDS = ["Ancient Bliss", "AncientBliss", "#AncientBliss"]

# Platform configuration
PLATFORMS = ["tiktok", "youtube", "instagram", "twitter", "facebook"]

# Google Drive configuration
DRIVE_FOLDER_BASE = "AncientBlissVideos"
DRIVE_CREDENTIALS_FILE = os.getenv("DRIVE_CREDENTIALS_FILE", "credentials.json")
DRIVE_TOKEN_FILE = os.getenv("DRIVE_TOKEN_FILE", "token.json")

# Google Drive root folder for uploads
DRIVE_ROOT_FOLDER_ID = os.getenv("DRIVE_ROOT_FOLDER_ID", "your-folder-id")

# Processing configuration
MAX_VIDEO_RESOLUTION = "1080p"
OUTPUT_FORMAT = "mp4"
TEMP_VIDEO_DIR = "./data/videos/temp"
PROCESSED_VIDEO_DIR = "./data/videos/processed"

# Scraping configuration
REQUEST_DELAY = 2  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# Deduplication configuration
DEDUP_THRESHOLD = 5  # Hash difference threshold for duplicates

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")




