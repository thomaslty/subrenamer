"""
Main window UI for SubRenamer application
"""

import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from typing import List, Dict
import os

class MainWindow:
    """Main window class handling the UI."""
    
    def __init__(self, root: tk.Tk, app):
        self.root = root
        self.app = app
        
        self.setup_ui()
        self.setup_drag_drop()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Drag & Drop Video and Subtitle Files", 
                               font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # File list frame
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Configure treeview style for better appearance
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=30)  # Add row padding
        style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Create treeview with 3 columns
        columns = ("video_file", "original_subtitle", "new_subtitle")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15, style="Custom.Treeview")
        
        # Configure alternating row colors for visual separation (after tree creation)
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')
        
        # Define column headings and properties
        self.tree.heading("video_file", text="Video File")
        self.tree.heading("original_subtitle", text="Original Subtitle")
        self.tree.heading("new_subtitle", text="Renamed Subtitle")
        
        # Set column widths (resizable)
        self.tree.column("video_file", width=250, minwidth=150)
        self.tree.column("original_subtitle", width=250, minwidth=150)
        self.tree.column("new_subtitle", width=250, minwidth=150)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid the treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Drop zone label (shown when empty)
        self.drop_label = ttk.Label(self.tree, text="Drop video and subtitle files here",
                                   font=("Arial", 14), foreground="gray")
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.E,), pady=(10, 0))
        
        # Buttons
        self.clear_button = ttk.Button(button_frame, text="Clear List", 
                                      command=self.app.clear_files)
        self.clear_button.grid(row=0, column=0, padx=(0, 10))
        
        self.submit_button = ttk.Button(button_frame, text="Submit", 
                                       command=self.app.process_rename)
        self.submit_button.grid(row=0, column=1)
        
        # Initially show drop label
        self.show_drop_label()
    
    def setup_drag_drop(self):
        """Set up drag and drop functionality."""
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.on_drop)
        
        # Also bind to the root window for better drop zone coverage
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """Handle file drop events."""
        files = self.root.tk.splitlist(event.data)
        # Filter for supported file types
        supported_files = []
        for file_path in files:
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                # Video extensions
                video_exts = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
                             '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.mts'}
                # Subtitle extensions
                subtitle_exts = {'.srt', '.ass', '.ssa', '.sub', '.vtt', '.sbv', '.dfxp'}
                
                if ext in video_exts or ext in subtitle_exts:
                    supported_files.append(file_path)
        
        if supported_files:
            self.app.add_files(supported_files)
    
    def show_drop_label(self):
        """Show the drop zone label when the list is empty."""
        self.drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def hide_drop_label(self):
        """Hide the drop zone label when files are present."""
        self.drop_label.place_forget()
    
    def update_file_list(self, matched_files: List[Dict]):
        """Update the file list display."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not matched_files:
            self.show_drop_label()
            return
        
        self.hide_drop_label()
        
        # Add matched files to the tree with alternating row colors
        for index, match in enumerate(matched_files):
            video_name = os.path.basename(match['video_file']) if match['video_file'] else ""
            original_sub = os.path.basename(match['subtitle_file']) if match['subtitle_file'] else ""
            new_sub = os.path.basename(match['new_subtitle_name']) if match['new_subtitle_name'] else ""
            
            # Apply alternating row colors for visual separation
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(video_name, original_sub, new_sub), tags=(tag,))