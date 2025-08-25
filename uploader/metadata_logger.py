# video_scraper_project/uploader/metadata_logger.py

import csv
import os
from datetime import datetime

class MetadataLogger:
    def __init__(self, log_file="./data/metadata_log.csv"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Initialize CSV file with headers if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'video_id', 'platform', 'source_url', 'filename', 
                    'upload_date', 'hashtags', 'dedup_status'
                ])
    
    def log_metadata(self, video_metadata, drive_file_id, dedup_status="original"):
        """Log video metadata to CSV file"""
        # Prepare hashtags as string
        hashtags = video_metadata.get('hashtags', [])
        if isinstance(hashtags, list):
            hashtags_str = ';'.join(hashtags)
        else:
            hashtags_str = str(hashtags)
        
        # Prepare row data
        row_data = [
            drive_file_id or 'N/A',
            video_metadata.get('platform', ''),
            video_metadata.get('source_url', ''),
            os.path.basename(video_metadata.get('file_path', '')),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            hashtags_str,
            dedup_status
        ]
        
        # Append to CSV
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)