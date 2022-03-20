import requests
import tibiapy


def getOnlinePlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.World.get_url(name)
            r = requests.post(url)
            content = r.text
            world = tibiapy.World.from_content(content)
            return world.online_players
        except Exception as e:
            print("Class Tibia.World.getOnlinePlayer: " + e.__str__())
            return None
