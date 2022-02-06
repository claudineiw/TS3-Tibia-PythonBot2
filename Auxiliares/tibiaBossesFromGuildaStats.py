from bs4 import BeautifulSoup
import requests
from BOT.funcoesBot import *
class tibiaBosses:
    def __init__(self,settings,semaforo):
        self.semaforo=semaforo
        self.settings=settings
        self.url="https://guildstats.eu/bosses?world={}&monsterName=&rook=0".format(self.settings["mundo"])

    def getHtml(self):
        try:
            sesion=requests.Session()
            page = sesion.get(self.url).text
            soup = BeautifulSoup(page, "html5lib")

            data = []
            table = soup.find('table', attrs={'class': 'tablesorter smallerFont'})
            rows = table.tbody.find_all("tr")
            for row in rows:
                name = row.find('a').text
                vistoPorUltimo=row.find_all('td')[7].text
                possibilidade = row.find_all('td')[9].text
                esperadoEm=row.find_all('td')[10].text

                monstro=[]
                if(possibilidade!="" or esperadoEm!=""):
                    if(possibilidade=="No" and esperadoEm!=""):
                        monstro.append(name)
                        monstro.append(vistoPorUltimo)
                        monstro.append(possibilidade)
                        if(esperadoEm==""):
                            monstro.append("-")
                        else:
                            monstro.append(esperadoEm)
                        data.append(monstro)
                    elif(possibilidade!="No" and esperadoEm==""):
                        monstro.append(name)
                        monstro.append(vistoPorUltimo)
                        monstro.append(possibilidade)
                        if (esperadoEm == ""):
                            monstro.append("-")
                        else:
                            monstro.append(esperadoEm)
                        data.append(monstro)

            listaOrdenada = sorted(data, key=lambda x: x[0])

            return listaOrdenada
        except:
            print("Erro Tibia Bosses")
            pass
            return None



    def trocarDescricaoCanal(self):
        lista=self.getHtml()
        if(not lista is None):
            novaDescricao = "[table][tr][td]Nome[/td][td]Ultima Aparicao      [/td][td]Chance                [/td][td]Esperando em[/td][/tr]"
            for itens in lista:
                novaDescricao += "[tr][td]{}[/td][td]{}[/td][td]{}[/td][td]{}[/td][/tr]".format(itens[0],itens[1],itens[2],itens[3])
            novaDescricao += "[/table]"
            descricao = self.tsconn.channelinfo(cid=pegarIdChannel(self.tsconn, self.settings["canalBoss"]))[0]["channel_description"]
            if descricao != novaDescricao:
                self.tsconn.channeledit(cid=pegarIdChannel(self.tsconn, self.settings["canalBoss"]),channel_description=novaDescricao)


    def iniciarBotCanalBoss(self):
        try:
            ultimo=0
            while(True):
                self.semaforo.acquire()
                self.tsconn = botsSecundarios(self.settings, "Bot-boss")
                agora=time.time()
                if(agora-ultimo>3600):
                    self.trocarDescricaoCanal()
                    ultimo=time.time()
                self.tsconn.close()
                self.semaforo.release()
                time.sleep(60)
        except:
            print("Erro bot canal boss")
            pass







