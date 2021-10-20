from BD.Character import Character
import Tibia.Character as CharacterTibia
import Tibia.Guild as GuildaTibia
import Tibia.World as WorldTibia
from BOT.AmigosEnimigos import AmigosEnimigos
from Auxiliares import data


class AtualizaOnlineELevel:
    def __init__(self, con):
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
        except Exception as e:
            self.todos = None
            return None

    def comGuilda(self):
        try:
            self.todos = Character.selectAll(self.con)
            if (not self.todos is type(None)):
                self.characterChecados = []
                guildaChecados = []
                morteNotificada = 1
                for player in self.todos :
                    if (player[5] != "None"):
                        guilda = player[5]
                        if (guilda not in guildaChecados):
                            if (guilda in AmigosEnimigos.selectGuildInimigas(self.con) or guilda in AmigosEnimigos.selectGuildAmigas(self.con)):
                                guildaOnline = GuildaTibia.getOnlinePlayer(guilda)
                                for playerGuilda in self.todos:
                                    if (playerGuilda[5] == guilda):
                                        for playerOnline in guildaOnline:
                                            if (playerOnline.name == playerGuilda[1]):
                                                playerCh = CharacterTibia.getPlayer(playerOnline.name)
                                                if (not playerCh is None):
                                                    if (len(playerCh.deaths) > 0):
                                                        dataMorteAtual = data.utc_to_local(playerCh.deaths[0].time)
                                                        if (dataMorteAtual == playerGuilda[7] and playerGuilda[9] == 1):
                                                            morteNotificada = 1
                                                        else:
                                                            morteNotificada = 0
                                                        Character.updatePorPlayer(playerOnline.name, playerOnline.level,
                                                                                  playerOnline.online,
                                                                                  playerOnline.vocation.name, guilda,
                                                                                  playerGuilda[6], self.con, dataMorteAtual,
                                                                                  playerCh.deaths[0].by_player, morteNotificada)
                                                    else:
                                                        Character.updatePorPlayer(playerOnline.name, playerOnline.level,
                                                                                  playerOnline.online,
                                                                                  playerOnline.vocation.name, guilda,
                                                                                  playerGuilda[6], self.con, playerGuilda[7],
                                                                                  playerGuilda[8], playerGuilda[9])
                                                    self.characterChecados.append(playerOnline.name)

                                guildaChecados.append(guilda)
        except Exception as e:
            print("Class AtualizaOnlineeLevel.comGuilda: "+e.__str__())
            self.todos=None
            return None



    def semGuildas(self):
        try:
            if (not self.todos is type(None)):
                if (len(self.todos) > 0):
                    world = WorldTibia.getOnlinePlayer(self.todos[0][6])
                    for player in self.todos:
                        if (player[1] in AmigosEnimigos.selectCharacterAmigos(self.con) or player[
                            1] in AmigosEnimigos.selectCharacterInimigos(self.con)):
                            if (player[5] == "None"):
                                for playerOnlineWorld in world:
                                    if (playerOnlineWorld.name == player[1]):
                                        playerCh = CharacterTibia.getPlayer(playerOnlineWorld.name)
                                        if (not playerCh is None):
                                            if (len(playerCh.deaths) > 0):
                                                dataMorteAtual2 = data.utc_to_local(playerCh.deaths[0].time)
                                                if (dataMorteAtual2 == player[7] and player[9] == 1):
                                                    morteNotificada = 1
                                                else:
                                                    morteNotificada = 0

                                                Character.updatePorPlayer(playerOnlineWorld.name, playerOnlineWorld.level, True,
                                                                          playerOnlineWorld.vocation.name, "None", player[6],
                                                                          self.con, dataMorteAtual2,
                                                                          playerCh.deaths[0].by_player, morteNotificada)
                                            else:

                                                Character.updatePorPlayer(playerOnlineWorld.name, playerOnlineWorld.level, True,
                                                                          playerOnlineWorld.vocation.name, "None", player[6],
                                                                          self.con, player[7], player[8], player[9])
                                            self.characterChecados.append(playerOnlineWorld.name)
        except Exception as e:
            print("Class AtualizaOnlineeLevel.semGuildas: " + e.__str__())
            self.todos = None
            return None

    def offlines(self):
        try:
            if (not self.todos is type(None)):
                for player in self.todos:
                    if (player[1] not in self.characterChecados):
                        Character.updatePorPlayer(player[1], player[2], False, player[4], player[5], player[6], self.con,
                                                  player[7], player[8], player[9])
        except Exception as e:
            print("Class AtualizaOnlineeLevel.offlines: " + e.__str__())
            self.todos = None
            return None