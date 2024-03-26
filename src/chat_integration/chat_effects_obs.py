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
import time
import random

sys.path.append('../../../discord-obs-integration/')

from discord_OBS_overlay_config import obs_host, obs_port, obs_password

# MINMAX_FOR_CC = {
#     'brightness': (,),
#     'contrast': (-4.0, 4.0),
#     'gamma': (-3.0, 3.0),
#     'hue': (,),
#     'saturation': (,),
# }

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
    print(f"Facecam is currently {'visible' if stuff.video_showing else 'inactive'}")
    print((stuff.attrs()))
    #TODO: Add command parsing for skewing (3d) and camera settings (gamma, hue, etc)
    # e.g. !cam gamma 1.0
    # e.g. !cam 90 90 90 (skewing in 3D)
    stuff2 = cl.get_source_filter(source_name="facecam", filter_name="Color Correction")
    print(stuff2.attrs())
    print(stuff2.filter_settings)
    # cl.set_source_filter_settings("facecam", "3D Effect", {'rot_x': 45.28, 'rot_y': 0.0, 'rot_z': 0.0}, overlay=True)
    # while True:
    #     try:
    #         cl.set_source_filter_settings("facecam", "3D Effect", {
    #                                   'rot_x': random.uniform(-50.0, 50.0),
    #                                   'rot_y': random.uniform(-50.0, 50.0),
    #                                   'rot_z': random.uniform(-50.0, 50.0)},
    #                                   overlay=True)
    #     except KeyboardInterrupt:
    #         break
    #     time.sleep(0.2)
    while True:
        _split_message_contents: list[str] = input(">> ").split(" ")
        if len(_split_message_contents) <= 1:
            print("fail!")
            continue
        try:
            match _split_message_contents[1]:
                case "skew":
                    cl.set_source_filter_settings("facecam", "3D Effect", {
                                            'rot_x': float(_split_message_contents[2]),
                                            'rot_y': float(_split_message_contents[3]),
                                            'rot_z': float(_split_message_contents[4])},
                                            overlay=True)

                case _chat_command_str if _chat_command_str in ['brightness', 'contrast', 'gamma', 'hue', 'saturation']:
                    print({("hue_shift" if _chat_command_str == "hue" else _chat_command_str): _split_message_contents[2]})
                    cl.set_source_filter_settings("facecam", "Color Correction", {
                    ("hue_shift" if _chat_command_str == "hue" else _chat_command_str): float(_split_message_contents[2])}, overlay=True)
                
                case "exit":
                    break

                case _:
                    print("fail!")

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(e)
    cl.disconnect()

# exit(0)
# chat = pytchat.create(video_id=get_stream_id())
# while chat.is_alive():
#     for c in chat.get().sync_items():
#         print(f"{c.datetime} [{c.author.name}]- {c.message}")
#         if c.message.startswith("!cam"):
#             _split_message_contents: list[str] = c.message.split(" ")
#             if not len(_split_message_contents) > 1:
#                 continue
#             try:
#                 match _split_message_contents[1]:
#                     case "skew":
#                         cl.set_source_filter_settings("facecam", "3D Effect", {
#                                                 'rot_x': _split_message_contents[2],
#                                                 'rot_y': _split_message_contents[3],
#                                                 'rot_z': _split_message_contents[4]},
#                                                 overlay=True)
#                     case _chat_command_str if _chat_command_str in ['brightness', 'contrast', 'gamma', 'hue', 'opacity', 'saturation']:
#                         cl.set_source_filter_settings("facecam", "Color Correction", {
#                     ("hue_shift" if _chat_command_str == "hue" else _chat_command_str): _split_message_contents[2]},
#                             overlay=True)
#             except Exception as e:
#                 print(e)
            # e.g. !cam gamma 1.0
            # e.g. !cam 90 90 90 (skewing in 3D)