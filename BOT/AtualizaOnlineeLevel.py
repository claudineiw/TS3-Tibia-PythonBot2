import asyncio

import Tibia.Character as CharacterTibia
import Tibia.Guild as GuildaTibia
import Tibia.World as WorldTibia
from Auxiliares import data
from BD.Character import Character
from BOT.AmigosEnimigos import AmigosEnimigos


class AtualizaOnlineELevel:
    def __init__(self, con):
        self.characterChecados = None
        self.todos = None
        print("Iniciou AtualizaOnlineELevel")
        self.con = con

    def iniciar(self):
        try:
            self.update()
        except:
            self.todos = None
            return None

    def update(self):
        try:
            self.comGuilda()
            self.semGuildas()
            self.offlines()
        except:
            self.todos = None
            return None

    def comGuilda(self):
        try:
            self.todos = Character.selectAll(self.con)
            if None is not self.todos:
                self.characterChecados = []
                guildaChecados = []
                # self.morteNotificada = 1
                for player in self.todos:
                    if player[5] != "None":
                        guilda = player[5]
                        if guilda not in guildaChecados:
                            if (guilda in AmigosEnimigos.selectGuildInimigas(
                                    self.con) or guilda in AmigosEnimigos.selectGuildAmigas(self.con)):
                               # guildaOnline = GuildaTibia.getOnlinePlayer(guilda)
                                guildaOnline = asyncio.run(GuildaTibia.get_character_online(guilda))
                                if None is not guildaOnline:
                                    for playerGuilda in self.todos:
                                        if playerGuilda[5] == guilda:
                                            for playerOnline in guildaOnline:
                                                if playerOnline.name == playerGuilda[1]:
                                                    playerCh = asyncio.run(CharacterTibia.get_character(playerOnline.name))
                                                    #playerCh = CharacterTibia.getPlayer(playerOnline.name)
                                                    if None is not playerCh:
                                                        if len(playerCh.deaths) > 0:
                                                            #dataMorteAtual = data.utc_to_local(playerCh.deaths[0].time)
                                                            if playerCh.deaths[0].__str__().replace("'","") == playerGuilda[7] and playerGuilda[9] == 1:
                                                                Character.updatePorPlayer(playerOnline.name,
                                                                                          playerOnline.level,
                                                                                          playerOnline.online,
                                                                                          playerOnline.vocation.name,
                                                                                          guilda,
                                                                                          playerGuilda[6], self.con,
                                                                                          playerGuilda[7],
                                                                                          playerGuilda[8],
                                                                                          playerGuilda[9])
                                                            else:
                                                                Character.updatePorPlayer(playerOnline.name,
                                                                                          playerOnline.level,
                                                                                          playerOnline.online,
                                                                                          playerOnline.vocation.name,
                                                                                          guilda,
                                                                                          playerGuilda[6], self.con,
                                                                                          playerCh.deaths[0].__str__().replace("'",""),
                                                                                          playerCh.deaths[0].by_player,
                                                                                          0)

                                                        else:
                                                            Character.updatePorPlayer(playerOnline.name,
                                                                                      playerOnline.level,
                                                                                      playerOnline.online,
                                                                                      playerOnline.vocation.name,
                                                                                      guilda,
                                                                                      playerGuilda[6], self.con,
                                                                                      playerGuilda[7],
                                                                                      playerGuilda[8], playerGuilda[9])
                                                        self.characterChecados.append(playerOnline.name)

                                    guildaChecados.append(guilda)
        except Exception as e:
            print("Class AtualizaOnlineeLevel.comGuilda: " + e.__str__())
            self.todos = None
            return None

    def semGuildas(self):
        try:
            if None is not self.todos:
                # self.morteNotificada=1
                if len(self.todos) > 0:
                   # world = WorldTibia.getOnlinePlayer(self.todos[0][6])
                    world = asyncio.run(WorldTibia.get_character_online(self.todos[0][6]))
                    for player in self.todos:
                        if player[1] in AmigosEnimigos.selectCharacterAmigos(self.con) or player[
                            1] in AmigosEnimigos.selectCharacterInimigos(self.con):
                            if player[5] == "None":
                                if None is not world:
                                    for playerOnlineWorld in world:
                                        if playerOnlineWorld.name == player[1]:
                                          #  playerCh = CharacterTibia.getPlayer(playerOnlineWorld.name)
                                            playerCh = asyncio.run(CharacterTibia.get_character(playerOnlineWorld.name))
                                            if None is not playerCh:
                                                if len(playerCh.deaths) > 0:
                                                   # dataMorteAtual2 = data.utc_to_local(playerCh.deaths[0].time)
                                                    if playerCh.deaths[0].__str__().replace("'","") == player[7] and player[9] == 1:
                                                        Character.updatePorPlayer(playerOnlineWorld.name,
                                                                                  playerOnlineWorld.level, True,
                                                                                  playerOnlineWorld.vocation.name,
                                                                                  "None", player[6],
                                                                                  self.con, player[7], player[8],
                                                                                  player[9])
                                                    else:
                                                        Character.updatePorPlayer(playerOnlineWorld.name,
                                                                                  playerOnlineWorld.level, True,
                                                                                  playerOnlineWorld.vocation.name,
                                                                                  "None", player[6],
                                                                                  self.con, playerCh.deaths[0].__str__().replace("'",""),
                                                                                  playerCh.deaths[0].by_player,
                                                                                  0)

                                                else:

                                                    Character.updatePorPlayer(playerOnlineWorld.name,
                                                                              playerOnlineWorld.level, True,
                                                                              playerOnlineWorld.vocation.name, "None",
                                                                              player[6],
                                                                              self.con, player[7], player[8], player[9])
                                                self.characterChecados.append(playerOnlineWorld.name)
        except Exception as e:
            print("Class AtualizaOnlineeLevel.semGuildas: " + e.__str__())
            self.todos = None
            return None

    def offlines(self):
        try:
            if None is not self.todos:
                for player in self.todos:
                    if player[1] not in self.characterChecados:
                        Character.updatePorPlayer(player[1], player[2], False, player[4], player[5], player[6],
                                                  self.con,
                                                  player[7], player[8], player[9])
        except Exception as e:
            print("Class AtualizaOnlineeLevel.offlines: " + e.__str__())
            self.todos = None
            return None
