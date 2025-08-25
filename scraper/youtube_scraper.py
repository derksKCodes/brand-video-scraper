# video_scraper_project/scraper/youtube_scraper.py
import yt_dlp
from scraper.base_scraper import BaseScraper
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import BRAND_NAME

class YouTubeScraper(BaseScraper):
    def __init__(self, api_key, download_dir="./data/videos/raw"):
        super().__init__("youtube", download_dir)
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos(self, query, max_results=50):
        """Search YouTube videos related to the brand"""
        try:
            search_response = self.youtube.search().list(
                q=f"{query} {BRAND_NAME}",
                part="snippet",
                maxResults=max_results,
                type="video",
                order="date"  # Get most recent first
            ).execute()
            
            video_urls = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_urls.append(video_url)
            
            return video_urls
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def extract_metadata(self, video_url):
        """Extract metadata from YouTube video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                metadata = {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'source_url': video_url,
                    'creator': info.get('uploader', ''),
                    'post_date': info.get('upload_date', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'tags': info.get('tags', []),
                    'hashtags': info.get('hashtags', []),
                }
                
                return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return None