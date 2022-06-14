import requests
import tibiapy
import aiohttp

async def get_character_online(name):
    try:
        status=0
        url = tibiapy.Character.get_url(name)
        async with aiohttp.ClientSession() as session:
            while status != 200:
                async with session.post(url) as resp:
                    status=resp.status
                    if(resp.status!=200):
                        continue
                    content = await resp.text()
        character = tibiapy.Character.from_content(content)
        return character.other_characters
    except Exception as e:
        print("Class Tibia.Character.get_character_online: " + e.__str__()+ " Nome: "+name)
        return None


async def get_character(name):
    try:
        status = 0
        url = tibiapy.Character.get_url(name)
        async with aiohttp.ClientSession() as session:
            while status != 200:
                async with session.post(url) as resp:
                    status = resp.status
                    if (resp.status != 200):
                        continue
                    content = await resp.text()
        character = tibiapy.Character.from_content(content)
        return character
    except Exception as e:
        print("Class Tibia.Character.get_character: " + e.__str__()+ " Nome: "+name)
        return None
