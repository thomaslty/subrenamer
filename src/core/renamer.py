"""
Subtitle file renaming functionality
"""

import os
import shutil
from typing import List, Dict
from pathlib import Path

class SubtitleRenamer:
    """Handles the actual renaming of subtitle files."""
    
    def rename_files(self, matched_files: List[Dict]) -> List[Dict]:
        """Rename subtitle files based on matched video files."""
        results = []
        
        for match in matched_files:
            if not match['subtitle_file'] or not match['new_subtitle_name']:
                continue
            
            original_path = match['subtitle_file']
            new_path = match['new_subtitle_name']
            
            result = {
                'original_path': original_path,
                'new_path': new_path,
                'success': False,
                'error': None
            }
            
            try:
                # Check if source file exists
                if not os.path.exists(original_path):
                    result['error'] = "Source file not found"
                    results.append(result)
                    continue
                
                # Check if target file already exists
                if os.path.exists(new_path) and original_path != new_path:
                    # If target exists and is different from source, ask user or skip
                    result['error'] = f"Target file already exists: {os.path.basename(new_path)}"
                    results.append(result)
                    continue
                
                # Perform the rename
                if original_path != new_path:
                    # Ensure target directory exists
                    target_dir = os.path.dirname(new_path)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Rename the file
                    shutil.move(original_path, new_path)
                    result['success'] = True
                else:
                    # Files are the same, mark as success
                    result['success'] = True
                
            except PermissionError:
                result['error'] = "Permission denied"
            except OSError as e:
                result['error'] = f"OS Error: {str(e)}"
            except Exception as e:
                result['error'] = f"Unexpected error: {str(e)}"
            
            results.append(result)
        
        return results
    
    def validate_rename_operation(self, matched_files: List[Dict]) -> Dict:
        """Validate rename operations before executing."""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        for match in matched_files:
            if not match['subtitle_file'] or not match['new_subtitle_name']:
                continue
            
            original_path = match['subtitle_file']
            new_path = match['new_subtitle_name']
            
            # Check if source exists
            if not os.path.exists(original_path):
                validation_result['errors'].append(
                    f"Source file not found: {os.path.basename(original_path)}"
                )
                validation_result['valid'] = False
            
            # Check if target already exists
            if os.path.exists(new_path) and original_path != new_path:
                validation_result['warnings'].append(
                    f"Target file exists and will be overwritten: {os.path.basename(new_path)}"
                )
            
            # Check write permissions on target directory
            target_dir = os.path.dirname(new_path)
            if not os.access(target_dir, os.W_OK):
                validation_result['errors'].append(
                    f"No write permission for directory: {target_dir}"
                )
                validation_result['valid'] = False
        
        return validation_result