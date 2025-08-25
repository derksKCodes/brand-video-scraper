# video_scraper_project/processing/video_deduplicator.py

import os
import imagehash
from PIL import Image
import cv2
import numpy as np

class VideoDeduplicator:
    def __init__(self, threshold=5):
        self.threshold = threshold
        self.known_hashes = {}
    
    def extract_video_frames(self, video_path, num_frames=3):
        """Extract representative frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Get frames at regular intervals
        frame_indices = [int(total_frames * (i / (num_frames + 1))) for i in range(1, num_frames + 1)]
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                # Convert to PIL Image for hashing
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                frames.append(pil_image)
        
        cap.release()
        return frames
    
    # def calculate_video_hash(self, video_path):
    #     """Calculate perceptual hash for a video"""
    #     frames = self.extract_video_frames(video_path)
    #     if not frames:
    #         return None
        
    #     # Calculate average hash of all frames
    #     hashes = [imagehash.average_hash(frame) for frame in frames]
    #     if not hashes:
    #         return None
        
    #     # Combine frame hashes into a single video hash
    #     combined_hash = hashes[0]
    #     for h in hashes[1:]:
    #         combined_hash = combined_hash | h  # Combine using OR operation
        
    #     return combined_hash
    

    def calculate_video_hash(self, video_path):
        """Calculate perceptual hash for a video"""
        frames = self.extract_video_frames(video_path)
        if not frames:
            return None
        
        # Calculate average hash of all frames
        hashes = [imagehash.average_hash(frame) for frame in frames]
        if not hashes:
            return None
        
        # Convert hashes to numpy arrays and average
        hash_arrays = np.array([h.hash for h in hashes])
        avg_hash = np.round(hash_arrays.mean(axis=0)).astype(bool)
        
        return imagehash.ImageHash(avg_hash)

    
    def is_duplicate(self, video_path):
        """Check if video is a duplicate of any known video"""
        video_hash = self.calculate_video_hash(video_path)
        if video_hash is None:
            return False, None
        
        # Compare with known hashes
        for known_path, known_hash in self.known_hashes.items():
            if video_hash - known_hash <= self.threshold:
                return True, known_path
        
        # Add to known hashes if not a duplicate
        self.known_hashes[video_path] = video_hash
        return False, None