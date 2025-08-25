# Video Scraping & Uploading for Brand

## 📌 Project Overview
This project automates the process of:
1. Scraping the internet for videos related to a brand.
2. Downloading and cleaning (e.g., removing watermarks, deduplicating) the videos.
3. Uploading the curated videos to a structured Google Drive folder.

The system ensures that only **unique, relevant, and brand-related** content is collected.

---

## 🚀 Features
- Scrapes videos from multiple platforms (TikTok, YouTube, Instagram, Twitter, etc.)
- Uses `yt-dlp` for robust video downloading.
- Automatic **watermark removal** using `ffmpeg`.
- Duplicate detection with **perceptual hashing** (`imagehash`).
- Organized uploads to **Google Drive** via API.
- Logging, error handling, and progress monitoring.

---

## 📂 Project Structure
```
video_scraper_project/
│── README.md                   # Documentation about setup & usage
│── requirements.txt             # Python dependencies
│── config.py                    # API keys, Drive folder IDs, brand name, etc.
│── run.py                       # Main entry point (orchestrates full pipeline)
│
├── scraper/
│   │── __init__.py
│   │── base_scraper.py          # Base class for scrapers (common utilities)
│   │── tiktok_scraper.py        # Scraper for TikTok videos
│   │── youtube_scraper.py       # Scraper for YouTube
│   │── instagram_scraper.py     # Scraper for Instagram
│   │── twitter_scraper.py       # Scraper for Twitter (X)
│   │── facebook_scraper.py      # Scraper for Facebook
│
├── processing/
│   │── __init__.py
│   │── watermark_removal.py     # Removes watermarks (ffmpeg/OpenCV)
│   │── video_deduplicator.py    # Detect & skip duplicate videos
│   │── video_converter.py       # Normalize resolution & format (e.g., 1080p MP4)
│
├── uploader/
│   │── __init__.py
│   │── drive_uploader.py        # Uploads videos to Google Drive
│   │── metadata_logger.py       # Saves metadata to CSV/JSON
│
├── utils/
│   │── __init__.py
│   │── helpers.py               # Helper functions (hashing, retries, logging)
│   │── validators.py            # Filters & validates brand-related content
│
└── data/
    │── input_urls.csv           # Optional: seed URLs/profiles
    │── metadata_log.csv         # Stores scraped video metadata
    │── videos/                  # Local downloaded video storage

```

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/video-scraper-uploader.git
cd video-scraper-uploader

2. Setup Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Requirements
pip install -r requirements.txt

---

🔑 Configuration

Create a .env file in the project root:

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_google_refresh_token
BRAND_KEYWORDS="ancient bliss, brand name variations"


Enable Google Drive API in Google Cloud Console.

Download OAuth credentials and place them as credentials.json.

---

▶️ Usage

Run Full Pipeline
python run.py

Run Individual Modules

Scraper only:

python scraper.py


Processor only:

python processor.py


Upload to Google Drive:

python uploader.py

---

📊 Evaluation

Logs provide detailed reports of scraped, removed, and uploaded videos.

Deduplication ensures no repeat videos.

All videos tagged with source URL + timestamp for traceability.

---

🛠️ Tech Stack

Scraping: yt-dlp, requests, selenium

Processing: ffmpeg, opencv-python, imagehash

Data Handling: pandas, numpy

Upload & Auth: pydrive2, google-api-python-client

Utils: tqdm, python-dotenv

---


📌 Notes

Only brand-related videos are retained (BRAND_KEYWORDS in .env).

For TikTok/Instagram scraping, cookies or API tokens may be required.

Ensure enough Google Drive space for uploads.

---


📜 License

MIT License