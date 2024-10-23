# File Integrity Monitoring (FIM) Tool

This repository contains a File Integrity Monitoring (FIM) tool that helps track changes in specified directories and mirror files to a backup location. 

## Configuration File (`config.json`)

The `config.json` file is crucial for configuring the FIM tool. Below is a detailed explanation of each key in the configuration file:

```json
{
    "directory_to_watch": "path/to/your/directory_to_watch",
    "log_file_path": "path/to/your/log.txt",
    "source_directory": "path/to/your/source_directory",
    "destination_directory": "path/to/your/destination_directory",
    "monitor_interval": 30,
    "file_whitelist": [],
    "file_blacklist": []
}

**directory_to_watch**:  
  This is where you specify the folder you want the FIM tool to keep an eye on for any changes. If anything is created, modified, deleted, or moved within this folder, the tool notify.
  **Example**: `"C:/path/to/your/watched_directory"`

- **log_file_path**:  
  This tells the tool where to save a log of all the monitoring events. Every time a file is created, changed, or deleted, the tool will write that information into this file, including the time it happened.  
  **Example**: `"C:/path/to/your/log.txt"`

- **source_directory**:  
  Here, you provide the path to the folder that contains the original files you want to back up. The FIM tool will check this folder for files that need to be copied over to another location.  
  **Example**: `"C:/path/to/your/source_directory"`

- **destination_directory**:  
  This is where the tool will place the backed-up files from the source directory. It’s helpful for keeping copies of your important files and can serve as a version history.  
  **Example**: `"C:/path/to/your/destination_directory"`

- **monitor_interval**:  
  This setting controls how often, in seconds, the FIM tool checks the source directory for new files to back up. A shorter interval means it will check more frequently, which could use more of your system’s resources.  
  **Example**: `30` (the tool will check every 30 seconds)

- **file_whitelist**:  
  This is a list of specific filenames that you always want the tool to monitor. If a file is included here, the tool will track it, no matter what other rules you have set.  
  **Example**: `["important_file.txt", "config.json"]`

- **file_blacklist**:  
  Conversely, this is a list of filenames that you want the tool to ignore. If a file is on this list, any changes to it won’t be tracked.  
  **Example**: `["blacklist.txt"]`
