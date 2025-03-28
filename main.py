import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set the directory to monitor (Change this to your actual Downloads folder path)
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")  # Works on Windows, macOS, and Linux

# File categorization based on extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".sql"],
    "Executables": [".exe", ".sh", ".bat", ".app"],
    "Others": []  # Uncategorized files
}

# Ensure all category folders exist
for category in FILE_CATEGORIES.keys():
    os.makedirs(os.path.join(DOWNLOADS_FOLDER, category), exist_ok=True)

def move_file(file_path):
    """Moves a file to the appropriate category folder."""
    if os.path.isdir(file_path):
        return  # Skip directories

    file_ext = os.path.splitext(file_path)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_ext in extensions:
            target_folder = os.path.join(DOWNLOADS_FOLDER, category)
            break
    else:
        target_folder = os.path.join(DOWNLOADS_FOLDER, "Others")

    # Move the file
    new_path = os.path.join(target_folder, os.path.basename(file_path))
    shutil.move(file_path, new_path)
    print(f"Moved: {file_path} → {new_path}")

def organize_existing_files():
    """Moves all existing files in Downloads to their respective folders."""
    print("📂 Organizing existing files...")
    for filename in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a folder
            move_file(file_path)
    print("✅ Existing files sorted!")

class DownloadHandler(FileSystemEventHandler):
    """Watches for new files in the Downloads folder."""
    def on_modified(self, event):
        """Triggered when a file is added or modified."""
        if event.is_directory:
            return
        move_file(event.src_path)

if __name__ == "__main__":
    # Organize all existing files on first run
    organize_existing_files()

    # Set up Watchdog observer
    observer = Observer()
    event_handler = DownloadHandler()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=True)

    print("📂 File Organizer is running... Monitoring Downloads folder.")
    observer.start()

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
