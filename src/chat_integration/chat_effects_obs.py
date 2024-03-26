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

import pytchat
import requests
import obsws
import re
import sys

sys.path.append('../../../discord-obs-integration/')

from discord_OBS_overlay_config import obs_host, obs_port, obs_password

youtube_link_regex = r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
ytlive_regex_f = re.compile(youtube_link_regex)


# print(raw_page_data[:10])
# print(ytlive_regex_f.findall(raw_page_data))
def get_stream_id():
    raw_page_data = requests.get("https://www.youtube.com/@okayxairen2/live").text
    for _r_match in ytlive_regex_f.findall(raw_page_data):
        if _r_match[2] == "?":
            return _r_match[3]

#TODO: Implement OBS side of thigs

if __name__ == "__main__":
    cl = obsws.ReqClient(host=obs_host, port=obs_port, password=obs_password, timeout=3)
    print("Connected to OBS instance running version", cl.get_version().obs_version)
    stuff = cl.get_source_active("facecam")
    print((stuff.attrs()))
    #TODO: Add command parsing for skewing (3d) and camera settings (gamma, hue, etc)
    # e.g. !cam gamma 1.0
    # e.g. !cam 90 90 90 (skewing in 3D)
    stuff2 = cl.get_source_filter(source_name="facecam", filter_name="3D Effect")
    print(stuff2.attrs())
    print(stuff2.filter_settings)
    cl.disconnect()
exit(0)
chat = pytchat.create(video_id=get_stream_id())
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")