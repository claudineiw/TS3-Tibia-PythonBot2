import requests
import tibiapy
import aiohttp

def getOnlinePlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Character.get_url(name)
            r = requests.post(url)
            content = r.text
            character = tibiapy.Character.from_content(content)
            return character.other_characters
        except Exception as e:
            #print("Class Tibia.Character.getOnlinePlayer: " + e.__str__())
            return None



async def get_character_online(name):
    try:
        url = tibiapy.Character.get_url(name)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content = await resp.text()
        character = tibiapy.Character.from_content(content)
        return character.other_characters
    except Exception as e:
        print("Class Tibia.Character.getOnlinePlayer: " + e.__str__())
        return None


async def get_character(name):
    try:
        url = tibiapy.Character.get_url(name)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content = await resp.text()
        character = tibiapy.Character.from_content(content)
        return character
    except Exception as e:
        print("Class Tibia.Character.getOnlinePlayer: " + e.__str__())
        return None

def getPlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Character.get_url(name)
            r = requests.post(url)
            content = r.text
            character = tibiapy.Character.from_content(content)
            return character
        except Exception as e:
            #print(name + " Class Tibia.Character.getPlayer: " + e.__str__())
            return None
