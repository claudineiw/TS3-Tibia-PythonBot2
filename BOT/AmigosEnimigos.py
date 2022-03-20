from BD.Character import Character
from BD.CharacterAmigos import CharacterAmigos
from BD.CharacterInimigos import CharacterInimigos
from BD.GuildAmigos import GuildAmigos
from BD.GuildInimigos import GuildInimigos
from Tibia import Guild


class AmigosEnimigos:
    def addGuildInimiga(self, name, con):
        guild = Guild.getGuild(name)
        if (guild is None):
            return (name + " Guild nao encontrada")
        else:
            addGuilda = GuildInimigos(guild.name, guild.world, con)
            return addGuilda.insert()

    def addGuildAmiga(self, name, con):
        guild = Guild.getGuild(name)
        if (guild is None):
            return (name + " Guild nao encontrada")
        else:
            addGuilda = GuildAmigos(guild.name, guild.world, con)
            return addGuilda.insert()

    def addCharacterInimigo(self, name, con):
        addCharinimigos = CharacterInimigos(name, con)
        return addCharinimigos.insert()

    def addCharacterAmigo(self, name, con):
        addCharAmigos = CharacterAmigos(name, con)
        return addCharAmigos.insert()

    @staticmethod
    def selectCharacterAmigos(con):
        return [tupla[0] for tupla in CharacterAmigos.select(con)]

    @staticmethod
    def deleteCharacterAmigos(name, con):
        idCharacter = Character.select(name, con)
        if (len(idCharacter) > 0):
            if (not CharacterAmigos.delete(idCharacter[0][0], con) is None):
                return True
            else:
                return (name + " amigo nao encontrado")
        else:
            return (name + " Personagem nao encontrado")

    @staticmethod
    def selectCharacterInimigos(con):
        return [tupla[0] for tupla in CharacterInimigos.select(con)]

    @staticmethod
    def deleteCharacterInimigos(name, con):
        idCharacter = Character.select(name, con)
        if (len(idCharacter) > 0):
            if (not CharacterInimigos.delete(idCharacter[0][0], con) is None):
                return True
            else:
                return (name + " inimigo nao encontrado")
        else:
            return (name + " Personagem nao encontrado")

    @staticmethod
    def selectGuildAmigas(con):
        return [tupla[0] for tupla in GuildAmigos.select(con)]

    @staticmethod
    def deleteGuildAmigas(name, con):
        idGuild = GuildAmigos.selectId(name, con)
        if (len(idGuild) != 0):
            if (not GuildAmigos.delete(idGuild[0][0], con) is None):
                return True
            else:
                return (name + " guilda amiga nao encontrada")
        else:
            return (name + " Guild nao encontrada")

    @staticmethod
    def selectGuildInimigas(con):
        return [tupla[0] for tupla in GuildInimigos.select(con)]

    @staticmethod
    def deleteGuildInimigas(name, con):
        idGuild = GuildInimigos.selectId(name, con)
        if (len(idGuild) != 0):
            if (not GuildInimigos.delete(idGuild[0][0], con) is None):
                return True
            else:
                return (name + " guilda inimiga nao encontrada")
        else:
            return (name + " Guild nao encontrada")
