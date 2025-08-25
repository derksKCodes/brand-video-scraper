# video_scraper_project/scraper/base_scraper.py

from abc import ABC, abstractmethod
import os
from urllib.parse import urlparse
import yt_dlp
from utils.helpers import retry, generate_video_hash
from utils.validators import filter_video_metadata

class BaseScraper(ABC):
    def __init__(self, platform_name, download_dir="./data/videos/raw"):
        self.platform_name = platform_name
        self.download_dir = os.path.join(download_dir, platform_name)
        os.makedirs(self.download_dir, exist_ok=True)
        
        # yt-dlp configuration
        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(id)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }
    
    @abstractmethod
    def search_videos(self, query, max_results=50):
        """Search for videos based on query"""
        pass
    
    @abstractmethod
    def extract_metadata(self, video_url):
        """Extract metadata from video URL"""
        pass
    
    @retry(max_retries=3, delay=2)
    def download_video(self, video_url):
        """Download video using yt-dlp"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Generate hash for deduplication
                video_hash = generate_video_hash(file_path)
                
                return {
                    'file_path': file_path,
                    'video_hash': video_hash,
                    'info': info
                }
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
    
    def process_video(self, video_url):
        """Full processing of a video: metadata extraction, validation, download"""
        # Extract metadata
        metadata = self.extract_metadata(video_url)
        if not metadata:
            return None
        
        # Validate if video is brand-related
        if not filter_video_metadata(metadata):
            return None
        
        # Download video
        download_result = self.download_video(video_url)
        if not download_result:
            return None
        
        # Combine metadata with download info
        metadata.update({
            'file_path': download_result['file_path'],
            'video_hash': download_result['video_hash'],
            'platform': self.platform_name
        })
        
        return metadata