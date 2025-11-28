import os
import glob

def cleanup_files_by_count(directories, max_files=10):
    """
    Keeps only the last `max_files` in the specified directories, deleting the oldest ones.
    
    Args:
        directories (list): List of directory paths to clean.
        max_files (int): Maximum number of files to keep per directory.
    """
    print(f"Starting cleanup. Keeping last {max_files} files per directory...")
    
    total_deleted = 0
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory not found, skipping: {directory}")
            continue
            
        # Get list of files with full paths
        files = glob.glob(os.path.join(directory, "*"))
        # Filter out directories, keep only files
        files = [f for f in files if os.path.isfile(f)]
        
        # Sort files by modification time (newest last)
        files.sort(key=os.path.getmtime)
        
        # Calculate how many to delete
        num_files = len(files)
        if num_files > max_files:
            num_to_delete = num_files - max_files
            files_to_delete = files[:num_to_delete]
            
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"Deleted old file: {filepath}")
                    total_deleted += 1
                except Exception as e:
                    print(f"Error deleting file {filepath}: {e}")
        else:
            print(f"Directory {directory} has {num_files} files (limit: {max_files}). No cleanup needed.")
                    
    print(f"Cleanup complete. Deleted {total_deleted} files.")
