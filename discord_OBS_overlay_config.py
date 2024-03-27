# Discord settings
discord_token = ""
valid_channels_list = [
    1051053710022815756,
    1142268841066504204,
]

# OBS settings
obs_host = '127.0.0.1' # this might be different if you're using a multi-computer setup
obs_port = 4455
obs_password = 'strongpassword123'
obs_channel_handle = '@okayxairen2'

# Web server settings
web_srv_flask_port = 24321





# Module setup

runner_modules = [
    {"dir": "src/server/", "file": "web_server_main.py", "label": "flask"},
    {"dir": "src/aggregator/", "file": "discord_aggregator.py", "label": "discord"},
    {"dir": "src/chat_integration/", "file": "chat_effects_obs.py", "label": "ytchat"}
]