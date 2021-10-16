import tibiapy
import requests

def getOnlinePlayer(name):
    if (name == ""):
        return None
    else:
        url = tibiapy.Character.get_url(name)
        r = requests.post(url)
        content = r.text
        try:
            character = tibiapy.Character.from_content(content)
            return character.other_characters
        except:
            return None


def getPlayer(name):
        if(name ==""):
            return None
        else:
            url = tibiapy.Character.get_url(name)
            r = requests.get(url)
            content = r.text
            try:
                character = tibiapy.Character.from_content(content)
                return character
            except:
                return None
