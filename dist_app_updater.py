import requests
import zipfile
import os
import sys
from io import BytesIO
import shutil

# from requests_toolbelt.utils import dump

def get_online_package_hash():
    _codeload_request = requests.head("https://codeload.github.com/Urufusan/discord-obs-integration/zip/refs/heads/main", headers={"User-Agent": "curl/7.81.0"})
    _etag = _codeload_request.headers.get("etag", "").strip().lstrip("W/").strip("\"")
    # print(dump.dump_all(_codeload_request).decode("utf-8"))
    return _etag

def get_local_package_hash():
    try:
        with open(".PACKAGEVER", "r") as _pverfile:
            _local_etag = _pverfile.read().strip()
        return _local_etag
    except:
        return "UNKNOWN"

def write_package_hash(etag_string):
    with open(".PACKAGEVER", "w") as _pverfile:
        _pverfile.write(etag_string)

def move_files_from_directory():
    source_dir = "discord-obs-integration-main"
    
    # Check if the source directory exists
    if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    # Get a list of files in the source directory
    os.system(f"cp -aR {source_dir}/* .")
    os.system("pip3 install flask flask-sock requests")
    # Remove the source directory
    try:
        shutil.rmtree(source_dir)
        print(f"Deleted the directory '{source_dir}'.")
    except Exception as e:
        print(f"Failed to delete the directory '{source_dir}': {str(e)}")
# Call the function to move files
# move_files_from_directory()


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
        sys.exit("Failed to download the zip file.")

if __name__ == "__main__":
    # URL of the zip file to download
    zip_url = "https://github.com/Urufusan/discord-obs-integration/archive/refs/heads/main.zip"
    print("Origin package hash:", _o_p_h := get_online_package_hash())
    print("Local package hash:", _l_p_h := get_local_package_hash())
    # exit()
    if _l_p_h != _o_p_h:
        # Call the function to download and extract the zip file
        download_and_extract_zip(zip_url)
        write_package_hash(_o_p_h)

