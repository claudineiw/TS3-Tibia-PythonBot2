import tibiapy
import requests

def getOnlinePlayer(name):
    if (name == ""):
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild.online_members
        except Exception as e:
            #print("Class Tibia.Guild.getOnlinePlayer: "+e.__str__()+" "+name)
            return None


def getAllPlayer(name):
    if (name == ""):
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild.members
        except Exception as e:
            #print("Class Tibia.Guild.getAllPlayer: " + e.__str__()+" "+name)
            return None

def getGuild(name):
    if(name==""):
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild
        except Exception as e:
            #print("Class Tibia.Guild.getGuild: " + e.__str__()+" "+name)
            return None