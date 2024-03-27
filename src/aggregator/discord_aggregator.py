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

import re
import sys

import discord
from discord.ext import commands

sys.path.append('../../../discord-obs-integration/')
import json
import os
from functools import cache

import requests

from discord_OBS_overlay_config import discord_token, valid_channels_list

if not discord_token:
    _fatal_err_message_token = "The Discord bot token was not provided in the config, please update your config!"
    print("!"*len(_fatal_err_message_token))
    print(_fatal_err_message_token)
    print("!"*len(_fatal_err_message_token))
    exit(1)

EMOJI_PATTERN = re.compile('<:[^:]+?:(\\d+)>')

weblink_rgx = r'('
# Scheme (HTTP, HTTPS, FTP and SFTP):
weblink_rgx += r'(?:(https?|s?ftp):\/\/)?'
 # www:
weblink_rgx += r'(?:www\.)?'
weblink_rgx += r'('
 # Host and domain (including ccSLD):
weblink_rgx += r'(?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)'
 # TLD:
weblink_rgx += r'([A-Z]{2,6})'
 # IP Address:
weblink_rgx += r'|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
weblink_rgx += r')'
 # Port:
weblink_rgx += r'(?::(\d{1,5}))?'
 # Query path:
weblink_rgx += r'(?:(\/\S+)*)'
weblink_rgx += r')'

weblink_rgx_searcher = re.compile(weblink_rgx, re.IGNORECASE)

# Regex to find the URL on the c.tenor.com domain that ends with .gif
tenor_rgx_searcher = re.compile(r"(?i)\b((https?://media1[.]tenor[.]com/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))[.]gif)")
# tenor_rgx_searcher = re.compile(r"https:\/\/media1\.tenor\.com\/m\/[\w\d]+\/[\w\-]+\.gif")

@cache
def get_gif_url_tenor(tenor_com_url: str):

    # Get the page content
    page_content = requests.get(url=tenor_com_url,
                                headers={
                                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                                    "DNT": "1",
                                    "Sec-GPC": "1",
                                }).text



    # Find and return the first match
    return tenor_rgx_searcher.search(page_content).group(0)


def get_web_url_from_str(raw_string: str) -> str:
    try:
        _r_match = weblink_rgx_searcher.search(raw_string)
        if _r_match:
            url = _r_match.group(0).strip()
            return url.rstrip(">").strip(")").strip("(")
        else:
            print("No valid web link found.")
    except Exception as e:
        print(f"Error: {e}")
    return ''


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='>>', intents=intents)

def is_dev():
    def check(ctx: commands.Context[commands.Bot]):
        return ctx.message.author.id in (
            667016884666761217,
            444785578152558592,
            523110570946199552,
        )

    return commands.check(check)


@client.event
async def on_ready(): 
    await client.change_presence(status=discord.Status.offline)
    print('Logged in as: {}'.format(client.user))


@client.event
async def on_message(ctx: discord.Message):
    # print(ctx.channel.id, ctx.content, ctx.author.name)
    if (ctx.channel.id not in valid_channels_list):
        if ctx.guild is None:
            if ctx.author.id in (444785578152558592, 940684920966250567):
                print("DM")
                pass
            else:
                return
        else:
            return

    
    
    if ctx.author == client.user:
        return
    if ctx.author.bot:
        return

    list_of_imgs = set()
    print(ctx.content)
    print(len(ctx.embeds))
    # print(ctx.embeds[0].url)
    # ctx.
    for attachment in ctx.attachments:
        if attachment.content_type.startswith("image"):
            list_of_imgs.add(attachment.url)
    
    for _sticker in ctx.stickers:
        list_of_imgs.add(_sticker.url)
    
    for embed_obj in ctx.embeds:
        print(embed_obj.to_dict())
        list_of_imgs.add(embed_obj.thumbnail.url)
    
    if bool(re.match(EMOJI_PATTERN, ctx.content)):
        buf = (int(EMOJI_PATTERN.findall(ctx.content)[0]))

        if buf:
            list_of_imgs.add(f"https://cdn.discordapp.com/emojis/{buf}.webp")
    
    if _temp_i_url := get_web_url_from_str(ctx.content):
        list_of_imgs.add(_temp_i_url)
    
    list_of_imgs.discard(None)
    list_of_imgs : list[str] = list(list_of_imgs)
    _final_json_list = []
    
    # Ruleset block
    for _image_url_i in list_of_imgs:
        if "cdn.discordapp.com/stickers/" in _image_url_i:
            _image_url_i = _image_url_i.replace("cdn.discordapp.com/stickers/", "media.discordapp.net/stickers/")
        if "media.tenor.com" in _image_url_i and (not _image_url_i.strip().endswith(".gif")):
            continue
        if "https://tenor.com" in _image_url_i:
            _image_url_i = get_gif_url_tenor(_image_url_i)
        if "media.discordapp.net" in _image_url_i:
            if "&hm=" not in _image_url_i:
                if "/stickers/" in _image_url_i:
                    pass
                else:
                    continue
        _final_json_list.append({'src': _image_url_i})
    
    if _final_json_list:
        print(_final_json_list)
        requests.post("http://127.0.0.1:5000/newimage", json=_final_json_list)
    # await ctx.reply('pong')

@client.hybrid_command(help="Restarts the bot", aliases=["btr", "butter"])
@is_dev()
async def restart(ctx: commands.Context[commands.Bot]):
    print("Bot forced to restart with a command. Restarting...")
    await ctx.reply(
        "The bot will perform a restart in a second! <:flushe:1161201649788915722>"
    )
    executable = sys.executable
    os.execl(executable, executable, *sys.argv)
    
if __name__ == "__main__":
    client.run(discord_token)