import time

from BD.Character import Character
import Tibia.Guild as GuildaTibia
from BOT.AmigosEnimigos import AmigosEnimigos
from BOT.AtualizaOnlineeLevel import AtualizaOnlineELevel


class AtualizaGuildas:
    def __init__(self, con):
        print("Iniciou AtualizaGuildas")
        self.con = con

    def iniciar(self):
        AtualizalevelEon = AtualizaOnlineELevel(self.con)
        while (True):
            try:
                self.update()
                self.removerPlayersGuilda()
                AtualizalevelEon.iniciar()
                time.sleep(30)
            except:
                pass

    def update(self):
        try:
            for guilda in AmigosEnimigos.selectGuildInimigas(self.con):
                guildaDados = GuildaTibia.getGuild(guilda)
                if(not guildaDados is None):
                    allPlayers=GuildaTibia.getAllPlayer(guilda)
                    for player in allPlayers:
                        char = Character(player.name, player.level, player.online, guildaDados.world, guildaDados.name,
                                         player.vocation.name, "0", 0, 1, self.con)
                        char.insert()


            for guilda in AmigosEnimigos.selectGuildAmigas(self.con):
                guildaDados = GuildaTibia.getGuild(guilda)
                if(not guildaDados is None):
                    allPlayers=GuildaTibia.getAllPlayer(guilda)
                    for player in allPlayers:
                        char = Character(player.name, player.level, player.online, guildaDados.world, guildaDados.name,
                                         player.vocation.name, "0", 0, 1, self.con)
                        char.insert()

        except Exception as e:
            print("Class AtualizaGuildas.update: "+e.__str__())
            return None

    def removerPlayersGuilda(self):
        try:
            for guilda in AmigosEnimigos.selectGuildAmigas(self.con):
                guildaDados = GuildaTibia.getAllPlayer(guilda)
                if(not guildaDados is None):
                    todosDaGuilda = Character.selectAllFromGuild(self.con, guilda)
                    for players in todosDaGuilda:
                        achou = False
                        for playerAtivo in guildaDados:
                            if (players[1] == playerAtivo.name):
                                achou = True
                                break
                        if (not achou):
                            Character.updatePorPlayer(players[1], players[2], players[3], players[4], None, players[6],self.con, players[7], players[8], players[9])

            for guilda in AmigosEnimigos.selectGuildInimigas(self.con):
                guildaDados = GuildaTibia.getAllPlayer(guilda)
                if(not guildaDados is None):
                    todosDaGuilda = Character.selectAllFromGuild(self.con, guilda)
                    for players in todosDaGuilda:
                        achou = False
                        for playerAtivo in guildaDados:
                            if (players[1] == playerAtivo.name):
                                achou = True
                                break
                        if (not achou):
                            Character.updatePorPlayer(players[1], players[2], players[3], players[4], None, players[6],self.con, players[7], players[8], players[9])


        except Exception as e:
            print("Class  AtualizaGuildas.removerPlayersGuilda: " + e.__str__())
            return None
