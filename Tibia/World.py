import tibiapy
import requests


def getOnlinePlayer(name):
    if (name == ""):
        return None
    else:
        url = tibiapy.World.get_url(name)
        r = requests.post(url)
        content = r.text
        try:
            world = tibiapy.World.from_content(content)
            return world.online_players
        except:
            return None
