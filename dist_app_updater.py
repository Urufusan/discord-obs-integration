import requests
import zipfile
import os
from io import BytesIO
import shutil

def move_files_from_directory():
    source_dir = "discord-obs-integration-main"
    
    # Check if the source directory exists
    if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    # Get a list of files in the source directory
    files = os.listdir(source_dir)
    
    # Move each file from the source directory to the current directory
    for file_name in files:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(os.getcwd(), file_name)
        
        # Check if the file is not a directory before moving
        if os.path.isfile(source_path):
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved '{file_name}' to the current directory.")
            except Exception as e:
                print(f"Failed to move '{file_name}': {str(e)}")
    # Remove the source directory
    try:
        os.rmdir(source_dir)
        print(f"Deleted the directory '{source_dir}'.")
    except Exception as e:
        print(f"Failed to delete the directory '{source_dir}': {str(e)}")
# Call the function to move files
move_files_from_directory()


def download_and_extract_zip(url):
    # Download the zip file from the provided URL
    print("Downloading updates...")
    response = requests.get(url)
    print("Updates downloaded.")
    if response.status_code == 200:
        # Read the content of the zip file
        zip_data = BytesIO(response.content)

        # Extract the files from the zip archive
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if "discord_OBS_overlay_config.py" not in file:  # Ignore config.py
                    print("Extracting:", file)
                    zip_ref.extract(file, os.getcwd())
        move_files_from_directory()
        print("Update completed successfully!")
    else:
        print("Failed to download the zip file.")

if __name__ == "__main__":
    # URL of the zip file to download
    zip_url = "https://github.com/Urufusan/discord-obs-integration/archive/refs/heads/main.zip"
    
    # Call the function to download and extract the zip file
    download_and_extract_zip(zip_url)
