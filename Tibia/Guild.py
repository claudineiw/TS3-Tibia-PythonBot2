import tibiapy
import requests

def getOnlinePlayer(name):
    if (name == ""):
        return None
    else:
        url = tibiapy.Guild.get_url(name)
        r = requests.post(url)
        content = r.text
        try:
            guild = tibiapy.Guild.from_content(content)
            return guild.online_members
        except:
            return None


def getAllPlayer(name):
    if (name == ""):
        return None
    else:
        url = tibiapy.Guild.get_url(name)
        r = requests.post(url)
        content = r.text
        try:
            guild = tibiapy.Guild.from_content(content)
            return guild.members
        except:
            return None

def getGuild(name):
    if(name==""):
        return None
    else:
        url = tibiapy.Guild.get_url(name)
        r = requests.post(url)
        content = r.text
        try:
            guild = tibiapy.Guild.from_content(content)
            return guild
        except:
            return None