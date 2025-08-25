# video_scraper_project/processing/video_converter.py

import os
import ffmpeg
from config import MAX_VIDEO_RESOLUTION, OUTPUT_FORMAT

class VideoConverter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def normalize_video(self, input_path, output_filename):
        """Convert video to standard format and resolution"""
        output_path = os.path.join(self.output_dir, f"{output_filename}.{OUTPUT_FORMAT}")
        
        try:
            # Probe input file
            probe = ffmpeg.probe(input_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                return None
            
            # Get current dimensions
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            
            # Calculate scaling dimensions while maintaining aspect ratio
            if MAX_VIDEO_RESOLUTION == "1080p":
                target_height = 1080
                target_width = int(width * (target_height / height))
            else:
                # Default to original dimensions
                target_width = width
                target_height = height
            # Ensure dimensions are divisible by 2
            target_width = target_width - (target_width % 2)
            target_height = target_height - (target_height % 2)    
            
            # Build ffmpeg command
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                vcodec='h264',
                acodec='aac',
                video_bitrate='5000k',
                audio_bitrate='192k',
                s=f"{target_width}x{target_height}",
                format=OUTPUT_FORMAT
            )
            
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            return output_path
            
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            return None
        except Exception as e:
            print(f"Error normalizing video: {e}")
            return None