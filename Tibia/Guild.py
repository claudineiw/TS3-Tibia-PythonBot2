from datetime import datetime

import requests
import tibiapy
from bs4 import BeautifulSoup


def getGuildBank(settings):
    try:
        mesAtual = datetime.now().astimezone().month
        guild = getGuild(settings["nomeGuilda"])

        url = 'https://www.tibia.com/account/'

        values = {'loginemail': settings["userTibia"],
                  'loginpassword': settings["senhaTibia"]}

        urlGuilda = "https://www.tibia.com/community/?subtopic=guilds&page=activitylog&world=" + guild.world + "&GuildName=" + guild.name.replace(
            " ", "+") + "&action=guildbankhistory"
        session = requests.Session()
        session.post(url, data=values)
        guilda = session.post(urlGuilda)
        soup = BeautifulSoup(guilda.text, "html5lib")
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
                    formatDate = "%b %d %Y, %H:%M:%S CET"
                    dataDepositoEmMinhaTimeZone = datetime.strptime(data[0], formatDate).astimezone()
                    if dataDepositoEmMinhaTimeZone.month == mesAtual:
                        data[0] = dataDepositoEmMinhaTimeZone.__str__()
                        datas.append(data)

        return datas
    except Exception as e:
        print("Class Tibia.Guild.getGuildBank: " + e.__str__())
        pass


def getOnlinePlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild.online_members
        except Exception:
            # print("Class Tibia.Guild.getOnlinePlayer: "+e.__str__()+" "+name)
            return None


def getAllPlayer(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild.members
        except Exception:
            # print("Class Tibia.Guild.getAllPlayer: " + e.__str__()+" "+name)
            return None


def getGuild(name):
    if name == "":
        return None
    else:
        try:
            url = tibiapy.Guild.get_url(name)
            r = requests.post(url)
            content = r.text
            guild = tibiapy.Guild.from_content(content)
            return guild
        except Exception:
            # print("Class Tibia.Guild.getGuild: " + e.__str__()+" "+name)
            return None
