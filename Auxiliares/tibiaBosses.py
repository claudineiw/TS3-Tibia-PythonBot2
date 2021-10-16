from bs4 import BeautifulSoup
from BOT.funcoesBot import *
import requests

s = requests.Session()
urlLoginTibiaBosses = "https://www.tibiabosses.com/wp-login.php"
ck = {'log': 'claudineiw', 'pwd': 'rj2td_mkyv3'}
s.post(urlLoginTibiaBosses, data=ck)


def cap(string):
    retorno = ""
    for itens in string.split():
        retorno += itens.capitalize() + " "
    return retorno

def tibiaBosses(settings):
    tsconn = botsSecundarios(settings,"Bot-boss")
    while True:
        try:
            tsconn.send_keepalive()
            url = "https://www.tibiabosses.com/" + settings["mundo"] + "/"
            page = s.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            listaRoshamuul = []
            listaArchdemons = []
            listaWeakBosses = []
            listaPoiBosses = []
            listaWithoutprediction = []
            listaWorldChanges = []
            listaProfitableBosses = []
            listaPremium = []

            Roshamuul = str(soup.find(text='Roshamuul Bosses').findNext('div').contents)
            Roshamuul = Roshamuul.replace("<i style=\"color:", "").replace(
                "<a href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in Roshamuul.splitlines():
                listaRoshamuul.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("[", "").strip().rstrip()))

            Archdemons = str(soup.find(text='Archdemons').findNext('div').contents)
            Archdemons = Archdemons.replace("<i style=\"color:", "").replace(
                "<a href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in Archdemons.splitlines():
                listaArchdemons.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").strip().rstrip()))

            WeakBosses = str(soup.find(text='Weak Bosses').findNext('div').contents)
            WeakBosses = WeakBosses.replace("<i style=\"color:", "").replace(
                "<a href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in WeakBosses.splitlines():
                listaWeakBosses.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("green;\">", "").replace("blue;\">", "").replace("]",
                                                                                                                  "").replace(
                        "-", " ").strip().rstrip()))

            POIBosses = str(soup.find(text='POI Bosses').findNext('div').contents)
            POIBosses = POIBosses.replace("<i style=\"color:", "").replace(
                "<a href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in POIBosses.splitlines():
                listaPoiBosses.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("[blue;\">", "").replace("blue;\">", "").replace("-",
                                                                                                                  " ").strip().rstrip()))

            Withoutprediction = str(soup.find(text='Without prediction').findNext('div').contents)
            Withoutprediction = Withoutprediction.replace("<i style=\"color:", "").replace(
                "href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in Withoutprediction.split("<a"):
                listaWithoutprediction.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("[blue;\">", "").replace("blue;\">", "").replace("-",
                                                                                                                  " ").strip().rstrip()
                    .replace(
                        "', <img alt=\"Here you can see how many days passed since Crustacea was killed (5 last kills). Since there are many spawning places of this boss it ican appear very often. You need to wait about 5 days for it to spawn in each spot. If the boss did not kill anybody, or it was not killed (missed, or catched as a mount) it would not appear on statistics. Click boss image if you want to read more about the boss.\" src=\"https://www.tibiabosses.com/wp content/uploads/2018/10/questionm.png\"/>, <br/>,",
                        "")
                    .replace("]", "").replace("[", "").replace("/", "")))

            WorldChanges = str(soup.find(text='World Changes').findNext('div').contents)
            WorldChanges = WorldChanges.replace("<i style=\"color:", "").replace(
                "href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace("', <br/>, ' '", "").replace(
                ", ' ', ", "")
            for itens in WorldChanges.split("<a"):
                listaWorldChanges.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("[blue;\">", "").replace("blue;\">", "").replace("-",
                                                                                                                  "").strip().rstrip().replace(
                        "', <img alt=\"White Deers killed in last 5 days  Enraged + Desperate\" src=\"https://www.tibiabosses.com/wpcontent/uploads/2018/10/questionm.png\"/>, <br/>,",
                        "")
                    .replace(
                        "', <img alt=\"Yielotaxes killed in last 5 days. Killing 2000 Yielotaxes on the server (can be done in couple days) triggers apperance of killable Raging Mage. Person who wants to kill the mage need to kill at least 250 Yielotaxes.\" src=\"https://www.tibiabosses.com/wpcontent/uploads/2018/10/questionm.png\"/>, <br/>,",
                        "")
                    .replace(
                        "', <img alt=\"Askaraks killed in last 5 days  Askarak Demons + Princes + Lords\" src=\"https://www.tibiabosses.com/wpcontent/uploads/2018/10/questionm.png\"/>, <br/>,",
                        "")
                    .replace(
                        "', <img alt=\"Shaburaks killed in last 5 days  Shaburak Demons + Princes + Lords\" src=\"https://www.tibiabosses.com/wpcontent/uploads/2018/10/questionm.png\"/>, <br/>,",
                        "")
                    .replace(
                        "', <img alt=\"Amount of killed Seacrest Serpents in last 5 days. When 3000 Seacrest Serpents have been killed across the server, a world change initiates (this happens the instant 3000 Seacrest Serpents have been killed). Renegade Quaras are appearing. After killing 1000 of Renegade Quaras, Seacrest Serpents are appearing again.\" src=\"https://www.tibiabosses.com/wpcontent/uploads/2018/10/questionm.png\"/>]",
                        "")
                    .replace("</a>,", "").replace("href=\"http://tibia.wikia.com/wiki/", "").replace("<br/>,",
                                                                                                     "").replace(";\">",
                                                                                                                 "").replace(
                        "[", "").replace("\n", "").replace("_", " ")))

            ProfitableBosses = str(soup.find(text='Profitable Bosses').findNext('div').contents)
            ProfitableBosses = ProfitableBosses.replace("<i style=\"color:", "").replace(
                "href=\"https://www.tibiabosses.com/bossopedia/", "").replace("\"><img src=\"", "").replace(
                "[green;\">", "").replace("red;\">", "").replace("</i>", "").replace(
                ", ' ', ", "")
            for itens in ProfitableBosses.split("<br/>"):
                listaProfitableBosses.append(cap(
                    itens.replace(itens[itens.find("https"):itens.rfind("</a>,")], "").replace("</a>, '", "").replace(
                        "   ,", "").replace("    ]", "").replace("[blue;\">", "").replace("blue;\">", "").replace("-",
                                                                                                                  " ").strip().rstrip()
                    .replace("', <div style=\"color: red;display: inline\">", "")
                    .replace("', <div style=\"color: green;display: inline\">", "")
                    .replace("</div>, '", "").replace("green;\">", "").replace("/", "").replace(", '", "").replace("',",
                                                                                                                   "")
                    .replace(
                        "<img alt=\"Midnight Panther is spawning every 3 4 days. Here you can see how many days passed since panther was killed (3 last kills). There are three spawning places of Midnight Panther. If the boss did not kill anybody, or it was not killed (missed, or catched as a mount) it would not appear on statistics. Click boss image if you want to read more about the boss.\" src=\"https:www.tibiabosses.comwp contentuploads201810questionm.png\">,",
                        "")
                    .replace(
                        "<img alt=\"There are 3 different spawns of White Pale. Here you can see how many days passed since the boss was killed on each spot. You need to wait at least 15 days for White Pale to spawn again in certain spot (treat each White Pale as different boss). If boss can spawn, number of passed days is presented in green colour. If it cannot   in red. Remember, that you need to figure out by yourself the spot on which White Pale was killed last time and on which places it could spawn. Click boss image for more details!\" src=\"https:www.tibiabosses.comwp contentuploads201810questionm.png\">,",
                        "")
                    .replace(
                        "<img alt=\"There are 4 different spawns of Rotworm Queen. Here you can see how many days passed since the boss was killed on each spot. You need to wait at least 14 days for Rotworm Queen to spawn again in certain spot (treat each Rotworm Queen as different boss). If boss can spawn, number of passed days is presented in green colour. If it cannot   in red. Remember, that you need to figure out by yourself the spot on which Rotworm Queen was killed last time and on which places it could spawn. Click boss image for more details!\" src=\"https:www.tibiabosses.comwp contentuploads201810questionm.png\">,",
                        "")
                    .replace(
                        "<img alt=\"There are two spawning places of Hirintror. Here you can see how many days ago Hirintror has been seen in two locations. Remember that you need to figure out on which spawn last Hirintror was killed on your server! Click Hirintror image for more informations about the boss.\" src=\"https:www.tibiabosses.comwp contentuploads201810questionm.png\">,",
                        "")
                    .replace("[", "").replace(", <a ", "").replace("<a ", "").replace(" ']", "").replace(",",
                                                                                                         "").replace(
                        "\n", "").strip().rstrip().replace("       ", " ")))

            premmiumBosses = str(soup.find(text='Premium Bosses').findNext('div').contents)
            premmiumBosses = premmiumBosses.replace("<i style=\"color:", "").replace(
                "href=\"https://www.tibiabosses.com/bossopedia/", "").replace("[green;\">", "").replace("red;\">",
                                                                                                        "").replace(
                "</i>", "").replace(", ' ', ", "")
            premmiumBosses = (
            premmiumBosses[:premmiumBosses.find("<a href=\"https://www.tibiabosses.com/Ferobra/history\"")])

            for itens in premmiumBosses.split("<br/>"):
                listaPremium.append(cap(itens.replace(itens[itens.find("https://"):itens.find("a>")], "")
                                             .replace(
                    "<img alt=\"There are two spawning places of Tyrn. Here you can see how many days ago Tyrn has been seen in two locations. Remember that you need to figure out on which spawn last Tyrn was killed on your server! Click Tyrn image for more informations about the boss.\" src=\"https://www.tibiabosses.com/wp-content/uploads/2018/10/questionm.png\"/>",
                    "")
                                             .replace("green;\">", "").replace("<a", "").replace(
                    "' ', <div class=\"execphpwidget\">", "").replace(">", "").replace("blue;\"", "")
                                             .replace(
                    "<img alt=\"Between April 3 and May 3 Yeti can appear on Chyllfroest. If Yeti was killed during the event it is still worth to check it on Folda! \" src=\"https://www.tibiabosses.com/wp-content/uploads/2018/10/questionm.png\"/",
                    "")
                                             .replace("[", "").replace("\n", "").rstrip().strip().replace("-",
                                                                                                          " ").replace(
                    "_", " ")).replace("\"<img Src=\"a", ""))

            try:
                listaRoshamuul.remove("")
            except:
                pass
            try:
                listaArchdemons.remove("")
            except:
                pass
            try:
                listaPoiBosses.remove("")
            except:
                pass
            try:
                listaWithoutprediction.remove("")
            except:
                pass
            try:
                listaWeakBosses.remove("")
            except:
                pass
            try:
                listaWorldChanges.remove("")
            except:
                pass
            try:
                listaProfitableBosses.remove("")
            except:
                pass
            try:
                listaPremium.remove("")
            except:
                pass

            listaTeste = []
            listaTeste.append(listaRoshamuul)
            listaTeste.append(listaArchdemons)
            listaTeste.append(listaPoiBosses)
            listaTeste.append(listaWithoutprediction)
            listaTeste.append(listaWeakBosses)
            listaTeste.append(listaWorldChanges)
            listaTeste.append(listaProfitableBosses)
            listaTeste.append(listaPremium)

            listaMob = []

            for lista in listaTeste:
                for itens in lista:
                    if itens.find("Chance") <= 10 and itens.find("Chance") != -1:
                        if itens.find("Expect") != -1:
                            chance = (itens[:itens.rfind("Chance") + 6])
                            nome = (itens[itens.rfind("Chance"):itens.find("Expect")].replace("Chance ", ""))
                            descricao = (itens[itens.find("Expect"):])
                            listaMob.append([chance.replace("No Chance", " [COLOR=red]Sem[/COLOR]").replace(
                                "High Chance", "[COLOR=green]Alta[/COLOR]").replace("Low Chance",
                                                                                    "[COLOR=blue]Baixa[/COLOR]"), nome,
                                             descricao])
                        elif itens.find("Last") != -1:
                            chance = (itens[:itens.rfind("Chance") + 6])
                            nome = (itens[itens.rfind("Chance"):itens.find("Last")].replace("Chance ", ""))
                            descricao = (itens[itens.find("Last"):])
                            listaMob.append([chance.replace("No Chance", " [COLOR=red]Sem[/COLOR]").replace(
                                "High Chance", "[COLOR=green]Alta[/COLOR]").replace("Low Chance",
                                                                                    "[COLOR=blue]Baixa[/COLOR]"), nome,
                                             descricao])

                    else:
                        if itens.find("Not Killed") != -1:
                            chance = "[COLOR=#aa55ff]Diario[/COLOR]"
                            nome = (itens[:itens.find("Not Killed")])
                            descricao = itens[itens.find("Not Killed"):]
                            listaMob.append([chance, nome, descricao])
                        elif itens.find("Killed") != -1:
                            chance = "[COLOR=#aa55ff]Diario[/COLOR]"
                            nome = (itens[:itens.find("Killed")])
                            descricao = itens[itens.find("Killed"):]
                            listaMob.append([chance, nome, descricao])
                        elif itens.find("|") != -1:
                            chance = "[COLOR=#f92eff]Variado[/COLOR]"
                            nome = (itens[:itens.find("|")])
                            descricao = itens[itens.find("|"):]
                            listaMob.append([chance, nome, descricao])
                        elif itens.find("Last Seen") != -1:
                            chance = "[COLOR=#f92eff]Variado[/COLOR]"
                            nome = (itens[:itens.find("Last Seen")])
                            descricao = itens[itens.find("Last Seen"):]
                            listaMob.append([chance, nome, descricao])

            listaMob = sorted(listaMob, key=lambda player: player[0], reverse=True)
            novaDescricao = "[table][tr][td]Chance[/td][td]Boss[/td][td]Ultima Aparicao/Proxima[/td][/tr]"
            for itens in listaMob:
                novaDescricao += "[tr][td]" + itens[0] + "[/td][td]" + itens[1] + "[/td][td]" + itens[2] + "[/td][/tr]"
            descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn,settings["canalBoss"]))[0][
                "channel_description"]
            if descricao != novaDescricao + "[/table]":
                tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalBoss"]),
                                   channel_description=novaDescricao + "[/table]")

            time.sleep(120)
        except:
                print("erro login tibia bosses")
                s.post(urlLoginTibiaBosses, data=ck)
        pass