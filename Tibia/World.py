import aiohttp
import tibiapy


async def get_character_online(name):
    try:
        status=0
        url = tibiapy.World.get_url(name)
        async with aiohttp.ClientSession() as session:
            while status != 200:
                async with session.post(url) as resp:
                    status=resp.status
                    if (resp.status != 200):
                        continue
                    content = await resp.text()
        world = tibiapy.World.from_content(content)
        return world.online_players
    except Exception as e:
        print("Class Tibia.World.get_character_online: " + e.__str__()+ " Nome: "+name)
        return None