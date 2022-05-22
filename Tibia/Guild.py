import asyncio
from datetime import datetime

import aiohttp
import tibiapy
from bs4 import BeautifulSoup


async def getGuildBank(settings):
    try:
        mesAtual = datetime.now().astimezone().month
        guild = await getGuild(settings["nomeGuilda"])

        url = 'https://www.tibia.com/account/'

        values = {'loginemail': settings["userTibia"],
                  'loginpassword': settings["senhaTibia"]}

        urlGuilda = "https://www.tibia.com/community/?subtopic=guilds&page=activitylog&world=" + guild.world + "&GuildName=" + guild.name.replace(
            " ", "+") + "&action=guildbankhistory"

       # session = requests.Session()
       # session.post(url, data=values)
        # guilda = session.post(urlGuilda)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=values) as resp:
                content = await resp.text()
            async with session.post(urlGuilda) as resp:
                content = await resp.text()



        soup = BeautifulSoup(content, "html5lib")
        table = soup.find('table', attrs={'class': 'TableContent'})
        rows = table.tbody.find_all("tr")
        datas = []
        for row in rows:
            colunas = row.find_all("td")
            data = []
            for col in colunas:
                if col.string == "Date":
                    break
                data.append(col.get_text().replace('\xa0', ' '))
            if len(data) > 0:
                if data[3] == "Deposit" and data[1] != '(deleted)':
                    try:
                        formatDate = "%b %d %Y, %H:%M:%S CEST"
                        dataDepositoEmMinhaTimeZone = datetime.strptime(data[0], formatDate).astimezone()
                    except:
                        formatDate = "%b %d %Y, %H:%M:%S CET"
                        dataDepositoEmMinhaTimeZone = datetime.strptime(data[0], formatDate).astimezone()
                    if dataDepositoEmMinhaTimeZone.month == mesAtual:
                        data[0] = dataDepositoEmMinhaTimeZone.__str__()
                        datas.append(data)

        return datas
    except Exception as e:
        print("Class Tibia.Guild.getGuildBank: " + e.__str__())
       # pass

async def get_character_online(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as resp:
                    content = await resp.text()
            guild = tibiapy.Guild.from_content(content)
            return guild.online_members
        except Exception as e:
            print("Class Tibia.Guild.getOnlinePlayer: "+e.__str__()+" "+name)
            return None



async def getAllPlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as resp:
                    content = await resp.text()
            guild = tibiapy.Guild.from_content(content)
            return guild.members
        except Exception as e:
            print("Class Tibia.Guild.getOnlinePlayer: "+e.__str__()+" "+name)
            return None


async def getGuild(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as resp:
                    content = await resp.text()
            guild = tibiapy.Guild.from_content(content)
            return guild
        except Exception as e:
            print("Class Tibia.Guild.getOnlinePlayer: "+e.__str__()+" "+name)
            return None

