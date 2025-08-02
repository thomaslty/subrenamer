"""
File matching logic for pairing video and subtitle files
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re
from difflib import SequenceMatcher

class FileMatcher:
    """Handles matching video files with subtitle files."""
    
    def __init__(self):
        self.video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                               '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.mts'}
        self.subtitle_extensions = {'.srt', '.ass', '.ssa', '.sub', '.vtt', '.sbv', '.dfxp'}
    
    def match_files(self, file_paths: List[str]) -> List[Dict]:
        """Match video files with subtitle files."""
        # Separate video and subtitle files
        video_files = []
        subtitle_files = []
        
        for file_path in file_paths:
            if not os.path.isfile(file_path):
                continue
                
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.video_extensions:
                video_files.append(file_path)
            elif ext in self.subtitle_extensions:
                subtitle_files.append(file_path)
        
        # Match files
        matches = []
        used_subtitles = set()
        
        for video_file in video_files:
            best_match = self._find_best_subtitle_match(video_file, subtitle_files, used_subtitles)
            
            if best_match:
                subtitle_file, confidence = best_match
                used_subtitles.add(subtitle_file)
                new_name = self._generate_new_subtitle_name(video_file, subtitle_file)
                
                matches.append({
                    'video_file': video_file,
                    'subtitle_file': subtitle_file,
                    'new_subtitle_name': new_name,
                    'confidence': confidence
                })
            else:
                # Video file without matching subtitle
                matches.append({
                    'video_file': video_file,
                    'subtitle_file': None,
                    'new_subtitle_name': None,
                    'confidence': 0.0
                })
        
        # Add unmatched subtitle files
        for subtitle_file in subtitle_files:
            if subtitle_file not in used_subtitles:
                matches.append({
                    'video_file': None,
                    'subtitle_file': subtitle_file,
                    'new_subtitle_name': None,
                    'confidence': 0.0
                })
        
        return matches
    
    def _find_best_subtitle_match(self, video_file: str, subtitle_files: List[str], 
                                 used_subtitles: set) -> Optional[Tuple[str, float]]:
        """Find the best matching subtitle file for a video file."""
        video_name = self._normalize_filename(os.path.splitext(os.path.basename(video_file))[0])
        
        best_match = None
        best_score = 0.0
        
        for subtitle_file in subtitle_files:
            if subtitle_file in used_subtitles:
                continue
                
            subtitle_name = self._normalize_filename(
                os.path.splitext(os.path.basename(subtitle_file))[0]
            )
            
            # Calculate similarity score
            score = self._calculate_similarity(video_name, subtitle_name)
            
            # Bonus for exact directory match
            if os.path.dirname(video_file) == os.path.dirname(subtitle_file):
                score += 0.1
            
            if score > best_score and score > 0.5:  # Minimum threshold
                best_score = score
                best_match = subtitle_file
        
        return (best_match, best_score) if best_match else None
    
    def _normalize_filename(self, filename: str) -> str:
        """Normalize filename for comparison."""
        # Remove common tags and patterns
        filename = re.sub(r'\\[.*?\\]', '', filename)  # Remove [tags]
        filename = re.sub(r'\\(.*?\\)', '', filename)  # Remove (tags)
        filename = re.sub(r'\\d{4}', '', filename)     # Remove years
        filename = re.sub(r'[._-]+', ' ', filename)    # Replace separators with spaces
        filename = re.sub(r'\\s+', ' ', filename)      # Normalize spaces
        return filename.strip().lower()
    
    def _calculate_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between two normalized filenames."""
        return SequenceMatcher(None, name1, name2).ratio()
    
    def _generate_new_subtitle_name(self, video_file: str, subtitle_file: str) -> str:
        """Generate new subtitle filename based on video filename."""
        video_dir = os.path.dirname(video_file)
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        subtitle_ext = os.path.splitext(subtitle_file)[1]
        
        # Use the video file's directory for the new subtitle
        new_subtitle_path = os.path.join(video_dir, video_name + subtitle_ext)
        return new_subtitle_path