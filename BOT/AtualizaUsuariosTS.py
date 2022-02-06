import time
from BD.Character import Character
from BD.usuarioTS import usuarioTS
from BD.BD import BD
from BOT import funcoesBot
from Auxiliares import canalOnline

class AtualizaUsuariosTS:
    def __init__(self, TScon, bdCon, usuarioTSs, settings, ListaDePermissoes):
        self.TScon = TScon
        self.usuarioTS = usuarioTSs
        self.bdCon = bdCon
        self.selectCharMain()
        self.settings = settings
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

        except Exception as e:
            print("Usuario nao encontrado no server TS: ")
            print("AtualizaUsuariosTS: " + e.__str__())
            print(usuarioTSs)
            pass


    def darPermissaoRegistrado(self):
        temMaior=0
        for itens in self.permissoesUsuario:
            perm=int(itens["sgid"])
            if(perm==int(self.settings["grupoConvidado"]) or perm==int(self.settings["grupoMestre"]) or perm==int(self.settings["grupoEditor"]) or perm==int(self.settings["grupoServerAdmin"]) or perm==int(self.settings["grupoAdmin"]) or perm==int(self.settings["grupoMovedor"])):
                temMaior=1
                break

        if(temMaior):
            self.removerPermissao(int(self.settings["grupoUsuario"]))
        else:
            self.adicionarPermissao(int(self.settings["grupoUsuario"]))

    def selectCharMain(self):
        char = Character.selectPorID(self.usuarioTS[2], self.bdCon)
        self.level = char[0][2]
        self.vocacao = char[0][4]
        self.online = char[0][3]


    def atualizaPermissoesLevel(self):
        for perm in self.ListaDePermissoes:
            if (int(perm["sgid"]) >= int(self.settings["permissaoLevelInicio"]) and int(perm["sgid"]) <= int(self.settings["permissaoLevelFim"])):
                if (self.level >= int(perm["name"].replace("+", "")) and int(
                        perm["name"].replace("+", "")) > self.level - 50):
                    self.adicionarPermissao(int(perm["sgid"]))
                else:
                    self.removerPermissao(int(perm["sgid"]))

    def atualizaOnlineOffline(self):
        if (self.online == 1):
            self.adicionarPermissao(int(self.settings["permissaoOnline"]))
            self.removerPermissao(int(self.settings["permissaoOffline"]))
        else:
            self.adicionarPermissao(int(self.settings["permissaoOffline"]))
            self.removerPermissao(int(self.settings["permissaoOnline"]))

    def atualizaTemMakereMakerOnline(self):
        if (self.usuarioTS[3] is None or len(self.usuarioTS[3]) == 0):
            self.removerPermissao(int(self.settings["permissaoTemMaker"]))
            self.removerPermissao(int(self.settings["permissaoMakerOnline"]))
        else:
            self.adicionarPermissao(int(self.settings["permissaoTemMaker"]))
            for maker in self.usuarioTS[3]:
                char = Character.selectPorID(maker, self.bdCon)
                onlineChar = char[0][3]
                if (onlineChar == 1):
                    self.adicionarPermissao(int(self.settings["permissaoMakerOnline"]))
                    return True

            self.removerPermissao(int(self.settings["permissaoMakerOnline"]))

    def atualizaVocacao(self):
        if ("knight" in self.vocacao.lower()):
            self.adicionarPermissao(int(self.settings["permissaoKnight"]))
            self.removerPermissao(int(self.settings["permissaoDruid"]))
            self.removerPermissao(int(self.settings["permissaoSorcerer"]))
            self.removerPermissao(int(self.settings["permissaoPaladin"]))
        else:
            if ("druid" in self.vocacao.lower()):
                self.adicionarPermissao(int(self.settings["permissaoDruid"]))
                self.removerPermissao(int(self.settings["permissaoKnight"]))
                self.removerPermissao(int(self.settings["permissaoSorcerer"]))
                self.removerPermissao(int(self.settings["permissaoPaladin"]))
            else:
                if ("paladin" in self.vocacao.lower()):
                    self.adicionarPermissao(int(self.settings["permissaoPaladin"]))
                    self.removerPermissao(int(self.settings["permissaoDruid"]))
                    self.removerPermissao(int(self.settings["permissaoSorcerer"]))
                    self.removerPermissao(int(self.settings["permissaoKnight"]))
                else:
                    if ("sorcerer" in self.vocacao.lower()):
                        self.adicionarPermissao(int(self.settings["permissaoSorcerer"]))
                        self.removerPermissao(int(self.settings["permissaoDruid"]))
                        self.removerPermissao(int(self.settings["permissaoKnight"]))
                        self.removerPermissao(int(self.settings["permissaoPaladin"]))

    def adicionarPermissao(self, idPermissao):
        try:
            self.TScon.servergroupaddclient(sgid=idPermissao, cldbid=self.dbIdUsuario)
        except :
            pass

    def removerPermissao(self, idPermissao):
        try:
            self.TScon.servergroupdelclient(sgid=idPermissao, cldbid=self.dbIdUsuario)
        except :
            pass


def atualizaUsuariosTsChamada(settings,semaforo):
    Bd = BD(settings, settings["userBDUpdateUserTS"])
    try:
        while (True):
           # semaforo.acquire()
            TScon = funcoesBot.botsSecundarios(settings, "Bot-UserTS")
            listaPermissoes = TScon.servergrouplist()
            for usuario in usuarioTS.select(Bd):
                AtualizaUsuariosTS(TScon, Bd, usuario, settings, listaPermissoes)

            canalOnline.CanalOnline(TScon, settings, Bd)
            TScon.close()
            #semaforo.release()
            time.sleep(30)
    except Exception as e:
        print("Error Atualiza Usuarios TS: "+e.__str__())
        pass
