import re
import discord
from discord.ext import commands
import sys
import os
import requests 
import json
from discord_OBS_overlay_config import discord_token, valid_channels_list

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


def get_gif_url_tenor(tenor_com_url: str):

    # Get the page content
    page_content = requests.get(url=tenor_com_url,
                                headers={
                                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                                    "DNT": "1",
                                    "Sec-GPC": "1",
                                }).text

    # Regex to find the URL on the c.tenor.com domain that ends with .gif
    regex = r"(?i)\b((https?://media1[.]tenor[.]com/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))[.]gif)"

    # Find and return the first match
    return re.findall(regex, page_content)[0][0]


def get_web_url_from_str(raw_string: str) -> str:
    global weblink_rgx_searcher
    try:
        print(weblink_rgx_searcher.search(raw_string).group(0).strip())
        itworks = True
    except:
        print("eh whatever")
        itworks = False
        pass

    if itworks:
        urlBF = weblink_rgx_searcher.search(raw_string)
        try:
            #url = 
            if urlBF.group(0).strip().endswith(">"): url = urlBF.group(0).strip()[:-1]
            else: url = urlBF.group(0).strip()
            buf = urlBF.group(3).strip()
            print(buf, url)
            return url.strip(")").strip("(")
        except:
            print('fail')
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
    if ctx.channel.id not in valid_channels_list:
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
    list_of_imgs = list(list_of_imgs)
    _final_json_list = []
    
    # Ruleset block
    for _image_url_i in list_of_imgs:
        if "https://tenor.com" in _image_url_i:
            _image_url_i = get_gif_url_tenor(_image_url_i)
        if "media.discordapp.net" in _image_url_i:
            if "&hm=" not in _image_url_i:
                continue
        _final_json_list.append({'src': _image_url_i})
    
    if list_of_imgs:
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
    

client.run(discord_token)