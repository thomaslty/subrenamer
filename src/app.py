"""
Main application class for SubRenamer
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .ui.main_window import MainWindow
from .core.file_matcher import FileMatcher
from .core.renamer import SubtitleRenamer

class SubRenamerApp:
    """Main application class."""
    
    def __init__(self):
        # Initialize TkinterDnD root window
        self.root = TkinterDnD.Tk()
        self.root.title("SubRenamer")
        self.root.geometry("900x600")
        
        # Set minimum window size
        self.root.minsize(600, 400)
        
        # Initialize components
        self.file_matcher = FileMatcher()
        self.renamer = SubtitleRenamer()
        
        # Initialize main window
        self.main_window = MainWindow(self.root, self)
        
        # Store matched files
        self.matched_files: List[Dict] = []
    
    def add_files(self, file_paths: List[str]) -> None:
        """Add files to the application and match them."""
        try:
            new_matches = self.file_matcher.match_files(file_paths)
            self.matched_files.extend(new_matches)
            self.main_window.update_file_list(self.matched_files)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process files: {str(e)}")
    
    def clear_files(self) -> None:
        """Clear all files from the list."""
        self.matched_files.clear()
        self.main_window.update_file_list(self.matched_files)
    
    def _validate_files(self) -> bool:
        """Validate that the number of video and subtitle files match."""
        if not self.matched_files:
            return False
            
        # Count video and subtitle files
        video_count = sum(1 for match in self.matched_files if match['video_file'] is not None)
        subtitle_count = sum(1 for match in self.matched_files if match['subtitle_file'] is not None)
        
        # Validation rule 2: Neither can be 0
        if video_count == 0:
            messagebox.showerror("Validation Error", "No video files found. Please add video files.")
            return False
            
        if subtitle_count == 0:
            messagebox.showerror("Validation Error", "No subtitle files found. Please add subtitle files.")
            return False
        
        # Validation rule 1: Counts must match
        if video_count != subtitle_count:
            messagebox.showerror(
                "Validation Error", 
                f"Number of video files ({video_count}) must match number of subtitle files ({subtitle_count})."
            )
            return False
            
        return True
    
    def process_rename(self) -> None:
        """Process the renaming of subtitle files."""
        if not self.matched_files:
            messagebox.showwarning("Warning", "No files to process.")
            return
        
        # Validate files before processing
        if not self._validate_files():
            return
        
        try:
            results = self.renamer.rename_files(self.matched_files)
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            if success_count == total_count:
                messagebox.showinfo("Success", f"Successfully renamed {success_count} files.")
            else:
                failed_files = [r['original_path'] for r in results if not r['success']]
                messagebox.showwarning(
                    "Partial Success", 
                    f"Renamed {success_count}/{total_count} files.\n"
                    f"Failed files: {', '.join(failed_files)}"
                )
            
            # Clear the list after processing
            self.clear_files()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename files: {str(e)}")
    
    def run(self):
        """Start the application."""
        self.root.mainloop()