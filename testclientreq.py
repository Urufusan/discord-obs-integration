import random
import time
import requests

# image1 = ""
while True:
    requests.post("http://127.0.0.1:5000/newimage", json=[random.choice([
                    {'src': "https://cdn.discordapp.com/emojis/1019850954151055390.gif?size=64&quality=lossless&name=SussyRock"}, 
                    {'src': 'https://cdn.discordapp.com/attachments/1051053710022815756/1215705719681056859/60440059.jpg?ex=65fdb92e&is=65eb442e&hm=541f86b937e39abf7d24548216cf90adf8ee4b6a5bf35a68f15bade8546dbf08&'},
                    {'src': 'https://cdn.discordapp.com/emojis/1122349994486280332.gif?size=96&quality=lossless'},
                    {'src': 'https://cdn.discordapp.com/emojis/804709588791197766.gif?size=96&quality=lossless'}
                    ])])
    time.sleep(random.uniform(0.1, 2.0))
