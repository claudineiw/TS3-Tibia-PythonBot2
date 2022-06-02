import asyncio

from BD.Character import Character as charBd
from Tibia import Character


class usuarioTS:
    def __init__(self, nomeTs, name, uidusuario, con):
        self.id = None
        self.con = con
        self.nomeTS = nomeTs
        self.name = name.replace("'", "\\'")
        self.uIdUsuario = uidusuario
        self.idChar = 0

    def get(self):
        return self.id

    @staticmethod
    def select(con):
        selecttodosUsuarios = "SELECT id, nomets, idcharactermain, idmakers, uidusuario	FROM usuariots order by nomets;"
        return con.select(selecttodosUsuarios)

    @staticmethod
    def selectUsuarioTSOnMain(idmain, con):
        selecttodosUsuarios = "SELECT id, nomets, idcharactermain, idmakers, uidusuario	FROM usuariots where idcharactermain={};".format(
            idmain)
        return con.select(selecttodosUsuarios)

    @staticmethod
    def selectUsuario(idUsuario, con):
        selecttodosUsuarios = "SELECT 'Nome TS: ',nomets, 'Nome Main: ',character.nome, 'UidUsuario: ',uidusuario FROM usuariots inner join character on (character.id=usuariots.idcharactermain) where usuariots.id={};".format(
            idUsuario)
        return con.select(selecttodosUsuarios)

    @staticmethod
    def selectMaker(idmaker, idmain, con):
        selecttodosUsuarios = "select 'Maker: ', (select nome from character where character.id={}),'Main: ',(select nome from character where character.id={});".format(
            idmaker, idmain)
        return con.select(selecttodosUsuarios)

    @staticmethod
    def deletePorCharacterMain(name, con):
        idMain = charBd.select(name, con)
        if len(idMain) == 0:
            return name + " personagem nao encontrado"
        else:
            sqldeleteInimigo = "delete FROM usuariots WHERE idcharactermain ={}".format(idMain[0][0])
            retorno = con.delete(sqldeleteInimigo)
            if retorno is None:
                return name + " nao encontrado em usuarios ts"
            else:
                return True

    @staticmethod
    def addMaker(main, maker, con):
        idMain = charBd.select(main, con)
        if len(idMain) == 0:
            return main + " Personagem nao encontrado confira o nome. E se estiver correto e nao pertencer a nenhuma guilda adicione como amigo primeiro"
        else:
            idMaker = charBd.select(maker, con)
            if len(idMaker) == 0:
                idMaker = charBd.insertPersonagem(maker, con)
                dadosMain = usuarioTS.selectUsuarioTSOnMain(idMain[0][0], con)
                if len(dadosMain) == 0:
                    return main + " Nao esta adicionado aos Usuarios do ts adicionar com !adduser"
                elif dadosMain[0][3] is None:
                    updateMakers = "UPDATE usuariots SET idmakers=array_append(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True
                elif idMaker[0][0] in dadosMain[0][3]:
                    return maker + " ja esta adicionado a lista de makers de: " + main
                else:
                    updateMakers = "UPDATE usuariots SET idmakers=array_append(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True
            else:
                dadosMain = usuarioTS.selectUsuarioTSOnMain(idMain[0][0], con)
                if len(dadosMain) == 0:
                    return main + " Nao esta adicionado aos Usuarios do ts adicionar com !adduser"
                elif dadosMain[0][3] is None:
                    updateMakers = "UPDATE usuariots SET idmakers=array_append(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True
                elif idMaker[0][0] in dadosMain[0][3]:
                    return maker + " ja esta adicionado a lista de makers de: " + main
                else:
                    updateMakers = "UPDATE usuariots SET idmakers=array_append(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True

    @staticmethod
    def rmMaker(main, maker, con):
        idMain = charBd.select(main, con)
        if len(idMain) == 0:
            return main + " Personagem nao encontrado confira o nome. E se estiver correto e nao pertencer a nenhuma guilda adicione como amigo primeiro"
        else:
            idMaker = charBd.select(maker, con)
            if len(idMaker) == 0:
                idMaker = charBd.insertPersonagem(maker, con)
                dadosMain = usuarioTS.selectUsuarioTSOnMain(idMain[0][0], con)
                if len(dadosMain) == 0:
                    return main + " Nao esta adicionado aos Usuarios do ts adicionar com !adduser"
                elif dadosMain[0][3] is None:
                    return main + " nao possui makers"

                elif idMaker[0][0] in dadosMain[0][3]:
                    updateMakers = "UPDATE usuariots SET idmakers=array_remove(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True
                else:
                    return maker + " nao esta na lista do main: " + main
            else:
                dadosMain = usuarioTS.selectUsuarioTSOnMain(idMain[0][0], con)
                if len(dadosMain) == 0:
                    return main + " Nao esta adicionado aos Usuarios do ts adicionar com !adduser"
                elif dadosMain[0][3] is None:
                    return main + " nao possui makers"

                elif idMaker[0][0] in dadosMain[0][3]:
                    updateMakers = "UPDATE usuariots SET idmakers=array_remove(idmakers,{}) WHERE idcharactermain={};".format(
                        idMaker[0][0], idMain[0][0])
                    con.update(updateMakers)
                    return True
                else:
                    return maker + " nao esta na lista do main: " + main

    def insert(self):
        sqlSelect = "SELECT id FROM Character WHERE nome ILIKE E'{}'".format(self.name)
        resultSelect = self.con.select(sqlSelect)
        if len(resultSelect) == 0:
            char = asyncio.run(Character.get_character(self.name))
            if char is None:
                return self.name + " personagem nao encontrado"
            else:
                addCharBd = charBd(char.name, char.level, 0, char.world, char.guild_name, char.vocation.name, "0", 0, 1,
                                   self.con)
                self.idChar = addCharBd.insert()
                self.name = char.name
                sqlInsertUsuarioTS = "INSERT INTO usuariots (nomets,idcharactermain,uidusuario) VALUES('{}',{},'{}')".format(
                    self.nomeTS, self.id, self.uIdUsuario)
                self.con.insert(sqlInsertUsuarioTS)
                return True
        else:
            self.id = resultSelect[0][0]
            sqlSelectUsuarioTS = "SELECT id FROM usuariots WHERE idcharactermain ={} and uidusuario='{}'".format(
                self.id, self.uIdUsuario)
            resultSelectInimigo = self.con.select(sqlSelectUsuarioTS)
            if len(resultSelectInimigo) > 0:
                return self.name + " Ja esta inserido em Usuario TS"
            else:
                sqlInsertUsuarioTS = "INSERT INTO usuariots (nomets,idcharactermain,uidusuario)  VALUES('{}',{},'{}')".format(
                    self.nomeTS, self.id, self.uIdUsuario)
                self.con.insert(sqlInsertUsuarioTS)
                return True
