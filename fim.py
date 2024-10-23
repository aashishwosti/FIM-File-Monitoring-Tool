import os
import hashlib
import time
import json
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load configuration settings from a JSON file
# This contains details like directories to monitor, whitelist/blacklist, etc.
with open(r'path\to\config.json', 'r') as f:
    config = json.load(f)

# Extract the necessary config variables for monitoring and logging
directory_to_watch = config['directory_to_watch']
log_file_path = config['log_file_path']
source_directory = config['source_directory']
destination_directory = config['destination_directory']
monitor_interval = config['monitor_interval']
file_whitelist = set(config['file_whitelist'])
file_blacklist = set(config['file_blacklist'])

# Function to calculate the MD5 hash of a file
# This helps in verifying file integrity (by comparing hashes)
def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        hash_md5 = hashlib.md5()
        # Read the file in chunks to avoid memory issues with large files
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to check if a file should be monitored
# Uses the whitelist/blacklist from the config to filter files
def is_file_monitored(file_path):
    file_name = os.path.basename(file_path)
    # If a whitelist exists and the file isn't in it, don't monitor
    if file_whitelist and file_name not in file_whitelist:
        return False
    # If the file is in the blacklist, don't monitor
    if file_name in file_blacklist:
        return False
    return True

# Function to log events (like file creation/deletion) with a timestamp
# Logs both to a file and prints it on the console
def log_event(event_message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{timestamp} - {event_message}\n")
    print(f"{timestamp} - {event_message}")

# Custom event handler class for monitoring filesystem changes
# We define what should happen when files are created, deleted, modified, or moved
class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            log_event(f"Directory created: {event.src_path}")
        else:
            if is_file_monitored(event.src_path):
                log_event(f"File created: {event.src_path}")
    
    def on_deleted(self, event):
        if event.is_directory:
            log_event(f"Directory deleted: {event.src_path}")
        else:
            if is_file_monitored(event.src_path):
                log_event(f"File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory and is_file_monitored(event.src_path):
            log_event(f"File modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory and is_file_monitored(event.src_path):
            log_event(f"File moved: from {event.src_path} to {event.dest_path}")

# Function to mirror the source directory to the destination directory
# It ensures that any new/modified files in the source are copied over to the destination
def mirror_directory(source, destination):
    # Walk through the source directory tree
    for root, dirs, files in os.walk(source):
        destination_dir = root.replace(source, destination)
        # Create the directory in the destination if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # For each file, calculate its hash and check if it's already mirrored
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, get_file_md5(source_file))
            if not os.path.exists(destination_file):
                # Copy the file to the destination if it doesn't exist there yet
                shutil.copy2(source_file, destination_file)
                log_event(f"File mirrored: {source_file} to {destination_file}")

# Main function to start directory monitoring and mirroring
def main():
    event_handler = MonitorHandler()
    observer = Observer()
    # Start monitoring the directory (and subdirectories) for file system changes
    observer.schedule(event_handler, path=directory_to_watch, recursive=True)
    observer.start()

    try:
        # Keep running the mirroring function at the specified interval
        while True:
            time.sleep(monitor_interval)
            mirror_directory(source_directory, destination_directory)
    except KeyboardInterrupt:
        # Gracefully stop the observer on manual interruption (Ctrl+C)
        observer.stop()

    observer.join()

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
