# video_scraper_project/run.py

import os
import time
from datetime import datetime
from config import PLATFORMS, BRAND_NAME
from scraper.youtube_scraper import YouTubeScraper
from processing.video_deduplicator import VideoDeduplicator
from processing.video_converter import VideoConverter
from uploader.drive_uploader import DriveUploader
from uploader.metadata_logger import MetadataLogger
from utils.helpers import setup_logger

def main():
    # Setup logging
    logger = setup_logger('main', './logs/main.log')
    
    # Initialize components
    deduplicator = VideoDeduplicator()
    converter = VideoConverter('./data/videos/processed')
    drive_uploader = DriveUploader()
    metadata_logger = MetadataLogger()
    
    # Initialize scrapers (example with YouTube)
    # In a real implementation, you would initialize all platform scrapers
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key:
        logger.error("YouTube API key not found")
        return
    
    youtube_scraper = YouTubeScraper(youtube_api_key)
    
    # Search for videos
    logger.info(f"Searching for videos related to {BRAND_NAME}")
    video_urls = youtube_scraper.search_videos(BRAND_NAME, max_results=20)
    logger.info(f"Found {len(video_urls)} potential videos")
    
    # Process each video
    for i, video_url in enumerate(video_urls):
        logger.info(f"Processing video {i+1}/{len(video_urls)}: {video_url}")
        
        try:
            # Extract metadata and download
            video_metadata = youtube_scraper.process_video(video_url)
            if not video_metadata:
                logger.info("Video not brand-related or failed to process")
                continue
            
            # Check for duplicates
            is_duplicate, original_path = deduplicator.is_duplicate(video_metadata['file_path'])
            if is_duplicate:
                logger.info(f"Duplicate detected, skipping: {video_metadata['file_path']}")
                metadata_logger.log_metadata(video_metadata, None, "duplicate")
                os.remove(video_metadata['file_path'])  # Remove duplicate file
                continue
            
            # Normalize video format
            output_filename = f"{video_metadata['platform']}_{os.path.basename(video_metadata['file_path']).split('.')[0]}"
            processed_path = converter.normalize_video(video_metadata['file_path'], output_filename)
            
            if not processed_path:
                logger.error(f"Failed to normalize video: {video_metadata['file_path']}")
                continue
            
            # Upload to Google Drive
            drive_file_id = drive_uploader.upload_file(processed_path, video_metadata['platform'])
            
            if drive_file_id:
                logger.info(f"Successfully uploaded to Drive with ID: {drive_file_id}")
                # Log metadata
                metadata_logger.log_metadata(video_metadata, drive_file_id, "original")
                
                # Clean up processed file
                os.remove(processed_path)
            else:
                logger.error("Failed to upload to Drive")
            
            # Clean up original file
            os.remove(video_metadata['file_path'])
            
            # Delay between processing to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error processing video {video_url}: {e}")
            continue
    
    logger.info("Processing completed")

if __name__ == "__main__":
    main()