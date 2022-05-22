import aiohttp
import tibiapy


async def get_character_online(name):
    try:
        url = tibiapy.World.get_url(name)
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:
                content = await resp.text()
        world = tibiapy.World.from_content(content)
        return world.online_players
    except Exception as e:
        print("Class Tibia.Character.getOnlinePlayer: " + e.__str__())
        return None