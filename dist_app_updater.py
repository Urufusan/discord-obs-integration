# Copyright (C) 2024 Urufusan
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import zipfile
import os
import sys
from io import BytesIO
import shutil
import platform

PROJECT_PARENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
# from requests_toolbelt.utils import dump
# TODO: Branch selection
def get_online_package_hash():
    _codeload_request = requests.head("https://codeload.github.com/Urufusan/discord-obs-integration/zip/refs/heads/main", headers={"User-Agent": "curl/7.81.0"})
    _etag = _codeload_request.headers.get("etag", "").strip().lstrip("W/").strip("\"")
    # print(dump.dump_all(_codeload_request).decode("utf-8"))
    return _etag

def get_local_package_hash():
    try:
        with open(f"{PROJECT_PARENT_FOLDER if __name__ != '__main__' else '.'}/.PACKAGEVER", "r") as _pverfile:
            _local_etag = _pverfile.read().strip()
        return _local_etag
    except Exception as e:
        print(e)
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
    os.system(f"{'pip3' if platform.system() != 'Windows' else 'py -m pip'} install flask flask-sock requests httpx httpx[http2] websocket-client")
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

def is_outdated():
    print("Origin package hash:", _o_p_h := get_online_package_hash())
    print("Local package hash: ", _l_p_h := get_local_package_hash())
    
    return _o_p_h != _l_p_h

if __name__ == "__main__":
    # URL of the zip file to download
    zip_url = "https://github.com/Urufusan/discord-obs-integration/archive/refs/heads/main.zip"
    print("Origin package hash:", _o_p_h := get_online_package_hash())
    print("Local package hash: ", _l_p_h := get_local_package_hash())
    # exit()
    if _l_p_h != _o_p_h:
        # Call the function to download and extract the zip file
        if not os.environ.get("DOBSCACHE"): download_and_extract_zip(zip_url)
        write_package_hash(_o_p_h)
    else:
        print("Local project files are up-to-date, there is nothing to update!")

