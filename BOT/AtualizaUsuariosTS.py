import asyncio
import time

from Auxiliares import canalOnline
from BD.BD import BD
from BD.Character import Character
from BD.usuarioTS import usuarioTS
from BOT import funcoesBot
from Tibia import Guild


class AtualizaUsuariosTS:
    def __init__(self, TScon, bdCon, usuarioTSs, settings, ListaDePermissoes, guildBankMes):
        self.online = None
        self.vocacao = None
        self.level = None
        self.nome = None
        self.TScon = TScon
        self.usuarioTS = usuarioTSs
        self.bdCon = bdCon
        self.selectCharMain()
        self.settings = settings
        self.guildBankMes = guildBankMes
        try:
            self.dbIdUsuario = self.TScon.clientdbfind(pattern=usuarioTSs[4], uid=True)[0]["cldbid"]
            self.dadosUsuario = self.TScon.clientdbinfo(cldbid=self.dbIdUsuario)[0]
            self.permissoesUsuario = self.TScon.servergroupsbyclientid(cldbid=self.dbIdUsuario)
            self.ListaDePermissoes = ListaDePermissoes

            self.darPermissaoRegistrado()
            self.atualizaPermissoesLevel()
            self.atualizaOnlineOffline()
            self.atualizaVocacao()
            self.atualizaTemMakereMakerOnline()
            self.guildBankPago()

        except Exception as e:
            print("Usuario nao encontrado no server TS: ")
            print("AtualizaUsuariosTS: " + e.__str__())
            print(usuarioTSs)
            pass

    def guildBankPago(self):
        try:
            if self.guildBankMes is not None:
                if len(self.guildBankMes) > 0:
                    pagou = 0
                    for user in self.guildBankMes:
                        if self.nome == user[1]:
                            pagou = 1

                    if pagou:
                        self.adicionarPermissao(int(self.settings["permissaoGuildBankPago"]))
                    else:
                        self.removerPermissao(int(self.settings["permissaoGuildBankPago"]))
        except:
            pass

    def darPermissaoRegistrado(self):
        temMaior = 0
        for itens in self.permissoesUsuario:
            perm = int(itens["sgid"])
            if (perm == int(self.settings["grupoConvidado"])
                    or perm == int(self.settings["grupoMestre"])
                    or perm == int(self.settings["grupoEditor"])
                    or perm == int(self.settings["grupoServerAdmin"])
                    or perm == int(self.settings["grupoAdmin"])
                    or perm == int(self.settings["grupoMovedor"])
                    or perm == int(self.settings["grupoLiderAliado"])
            ):
                temMaior = 1
                break

        if temMaior:
            self.removerPermissao(int(self.settings["grupoUsuario"]))
        else:
            self.adicionarPermissao(int(self.settings["grupoUsuario"]))

    def selectCharMain(self):
        char = Character.selectPorID(self.usuarioTS[2], self.bdCon)
        self.nome = char[0][1]
        self.level = char[0][2]
        self.vocacao = char[0][4]
        self.online = char[0][3]

    def atualizaPermissoesLevel(self):
        for perm in self.ListaDePermissoes:
            if int(self.settings["permissaoLevelInicio"]) <= int(perm["sgid"]) <= int(
                    self.settings["permissaoLevelFim"]):
                if self.level >= int(perm["name"].replace("+", "")) > self.level - 50:
                    self.adicionarPermissao(int(perm["sgid"]))
                else:
                    self.removerPermissao(int(perm["sgid"]))

    def atualizaOnlineOffline(self):
        if self.online == 1:
            self.adicionarPermissao(int(self.settings["permissaoOnline"]))
            self.removerPermissao(int(self.settings["permissaoOffline"]))
        else:
            self.adicionarPermissao(int(self.settings["permissaoOffline"]))
            self.removerPermissao(int(self.settings["permissaoOnline"]))

    def atualizaTemMakereMakerOnline(self):
        if self.usuarioTS[3] is None or len(self.usuarioTS[3]) == 0:
            self.removerPermissao(int(self.settings["permissaoTemMaker"]))
            self.removerPermissao(int(self.settings["permissaoMakerOnline"]))
        else:
            self.adicionarPermissao(int(self.settings["permissaoTemMaker"]))
            for maker in self.usuarioTS[3]:
                char = Character.selectPorID(maker, self.bdCon)
                onlineChar = char[0][3]
                if onlineChar == 1:
                    self.adicionarPermissao(int(self.settings["permissaoMakerOnline"]))
                    return True

            self.removerPermissao(int(self.settings["permissaoMakerOnline"]))

    def atualizaVocacao(self):
        if "knight" in self.vocacao.lower():
            self.adicionarPermissao(int(self.settings["permissaoKnight"]))
            self.removerPermissao(int(self.settings["permissaoDruid"]))
            self.removerPermissao(int(self.settings["permissaoSorcerer"]))
            self.removerPermissao(int(self.settings["permissaoPaladin"]))
        else:
            if "druid" in self.vocacao.lower():
                self.adicionarPermissao(int(self.settings["permissaoDruid"]))
                self.removerPermissao(int(self.settings["permissaoKnight"]))
                self.removerPermissao(int(self.settings["permissaoSorcerer"]))
                self.removerPermissao(int(self.settings["permissaoPaladin"]))
            else:
                if "paladin" in self.vocacao.lower():
                    self.adicionarPermissao(int(self.settings["permissaoPaladin"]))
                    self.removerPermissao(int(self.settings["permissaoDruid"]))
                    self.removerPermissao(int(self.settings["permissaoSorcerer"]))
                    self.removerPermissao(int(self.settings["permissaoKnight"]))
                else:
                    if "sorcerer" in self.vocacao.lower():
                        self.adicionarPermissao(int(self.settings["permissaoSorcerer"]))
                        self.removerPermissao(int(self.settings["permissaoDruid"]))
                        self.removerPermissao(int(self.settings["permissaoKnight"]))
                        self.removerPermissao(int(self.settings["permissaoPaladin"]))

    def adicionarPermissao(self, idPermissao):
        try:
            self.TScon.servergroupaddclient(sgid=idPermissao, cldbid=self.dbIdUsuario)
        except:
            pass

    def removerPermissao(self, idPermissao):
        try:
            self.TScon.servergroupdelclient(sgid=idPermissao, cldbid=self.dbIdUsuario)
        except:
            pass


def atualizaUsuariosTsChamada(settings, semaforo):
    Bd = BD(settings, settings["userBDUpdateUserTS"])
    while True:
        TScon = funcoesBot.botsSecundarios(settings, "Bot-UserTS")
        try:
            semaforo.acquire()
            listaPermissoes = TScon.servergrouplist()
            guildBankMes = asyncio.run(Guild.getGuildBank(settings))
            for usuario in usuarioTS.select(Bd):
                AtualizaUsuariosTS(TScon, Bd, usuario, settings, listaPermissoes, guildBankMes)

            canalOnline.CanalOnline(TScon, settings, Bd)
            TScon.close()
            semaforo.release()
            time.sleep(30)
        except Exception as e:
            TScon.close()
            semaforo.release()
            time.sleep(30)
            print("Error Atualiza Usuarios TS: " + e.__str__())
            pass
