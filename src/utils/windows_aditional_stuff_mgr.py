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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

_CMD_CONSTANT = "cmd.exe /c "

def convert_win_path_to_unix_path(_path_plain: str) -> str:
    """
    Converts path that bash will accept
    """
    _path_plain = _path_plain.strip()
    return (_path_plain[0].lower() + _path_plain[2:]).replace("\\", "/")
    

def get_cmder():
    """
    Downloads and sets up the Cmder shell and runtime
    """
    os.system(_CMD_CONSTANT + "mkdir %temp%\\cmder")
    # print(os.chdir(os.getenv('TEMP')))
    os.system(_CMD_CONSTANT + "curl -L -o %temp%/cmder.zip https://github.com/cmderdev/cmder/releases/download/v1.3.24/cmder.zip")
    os.system(_CMD_CONSTANT + "tar -xvf cmder.zip -C %temp%/cmder")

def run_self_under_cmder(_target_pwd: str, _target_file: str):
    """
    Execute RUNME.py under Cmder
    """
    os.system(_CMD_CONSTANT + f'%temp%\\cmder\\vendor\\git-for-windows\\bin\\sh.exe -c "cd \'{convert_win_path_to_unix_path(_target_pwd)}\' && py \'{convert_win_path_to_unix_path(_target_file)}\'"')

def check_if_shell_exists():
    _shell_location = f"{os.getenv('TEMP')}\\cmder\\vendor\\git-for-windows\\bin\\sh.exe"
    return (os.path.exists(_shell_location) and os.path.isfile(_shell_location))

def windows_install_procedure(_target_pwd: str, _target_file: str):
    if check_if_shell_exists():
        pass
    else:
        get_cmder()
    run_self_under_cmder(_target_pwd, _target_file)