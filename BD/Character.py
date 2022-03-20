from BD.Guild import Guild
from BD.Vocation import Vocation
from BD.World import World
from Tibia.Character import getPlayer


class Character:
    def __init__(self, name, level, online, world, guild, vocation, ultimaMorte, ultimaMorteMobOuPlayer,
                 ultimaMorteNotificada, con):
        self.con = con
        self.name = name.replace("'", "\\'")
        self.level = level
        self.online = online

        if online:
            self.online = 1
        else:
            self.online = 0

        self.ultimaMorte = ultimaMorte
        wor = World(world, con)
        self.world = wor.insert()
        guid = Guild(guild, world, con)
        self.guild = guid.insert()
        voc = Vocation(vocation, con)
        self.vocation = voc.insert()

        if ultimaMorteMobOuPlayer:
            self.ultimaMorteMobOuPlayer = 1
        else:
            self.ultimaMorteMobOuPlayer = 0

        self.ultimaMorteNotificada = ultimaMorteNotificada
        self.id = 0

    def get(self):
        return self.id

    @staticmethod
    def insertPersonagem(name, con):
        resultSelect = Character.select(name, con)
        if len(resultSelect) == 0:
            char = getPlayer(name)
            if char is None:
                return []
            else:
                addCharBd = Character(char.name, char.level, 0, char.world, char.guild_name, char.vocation.name, "0", 0,
                                      1, con)
                return addCharBd.insert()

    @staticmethod
    def select(name, con):
        if "\'" not in name:
            name = name.replace("'", "\\'")
        sqlSelect = "SELECT id FROM Character WHERE nome ILIKE E'{}'".format(name)
        return con.select(sqlSelect)

    @staticmethod
    def selectPorID(idSelect, con):
        sqlSelect = "SELECT Character.id,Character.nome,level,online,Vocations.nome FROM Character inner join world on(character.worldid=world.id) inner join Guild on Character.guildid=Guild.id   inner join vocations on (character.vocationid=vocations.id)	where Character.id={}".format(
            idSelect)
        return con.select(sqlSelect)

    @staticmethod
    def selectAll(con):
        sqlSelect = '''SELECT Character.id,Character.nome,level,online,Vocations.nome,Guild.nome,World.nome,Character.ultimaMorte ,Character.ultimaMorteMobOuPlayer ,Character.ultimaMorteNotificada 
                        FROM Character 
                        inner join world on(character.worldid=world.id)
                        inner join Guild on Character.guildid=Guild.id 
                        inner join vocations on (character.vocationid=vocations.id)
                        where  Guild.id in (select guildid from guildinimiga) or Guild.id in (select guildid from guildamiga) or Character.id in (SELECT characterid FROM public.characterinimigo ) or Character.id in (SELECT characterid FROM public.characteramigo )
                        order by character.nome  '''
        return con.select(sqlSelect)

    @staticmethod
    def selectAllFromGuild(con, guild):
        sqlSelect = "SELECT Character.id,Character.nome,level,online,Vocations.nome,Guild.nome,World.nome,Character.ultimaMorte ,Character.ultimaMorteMobOuPlayer ,Character.ultimaMorteNotificada FROM Character inner join Guild on Character.guildid=Guild.id inner join World on Guild.worldId=World.id inner join Vocations on vocationId = Vocations.id where Guild.nome ILIKE E'{}'".format(
            guild)
        return con.select(sqlSelect)

    @staticmethod
    def selectAllFromGuilOnline(con, guild):
        sqlSelect = "SELECT Character.id,Character.nome,level,online,Vocations.nome,Guild.nome,World.nome,Character.ultimaMorte ,Character.ultimaMorteMobOuPlayer ,Character.ultimaMorteNotificada FROM Character inner join Guild on Character.guildid=Guild.id inner join World on Guild.worldId=World.id inner join Vocations on vocationId = Vocations.id where Guild.nome ILIKE E'{}' and online=1 ORDER BY Character.nome".format(
            guild)
        return con.select(sqlSelect)

    @staticmethod
    def selectTotalPlayersGuild(con, guild):
        sqlSelect = "SELECT count(Character.id) FROM Character inner join Guild on Character.guildid=Guild.id  where Guild.nome ILIKE E'{}'".format(
            guild)
        return con.select(sqlSelect)

    def insert(self):
        result = self.select(self.name, self.con)
        if len(result) == 0:
            sqlinsert = "INSERT INTO Character (nome, level,online,vocationId,guildId,worldId,ultimaMorte,ultimaMorteMobOuPlayer,ultimaMorteNotificada) VALUES(E'{}',{},{},{},{},{},'{}',{},{})".format(
                self.name, self.level, self.online, self.vocation, self.guild, self.world, self.ultimaMorte,
                self.ultimaMorteMobOuPlayer, self.ultimaMorteNotificada)
            self.id = self.con.insert(sqlinsert)
            return self.id
        else:
            self.id = result[0][0]
            sqlUpdate = "UPDATE Character SET level = {} , online = {} ,vocationId = {}, guildId = {}, worldId = {} WHERE id = {}".format(
                self.level, self.online, self.vocation, self.guild, self.world, self.id)
            self.con.update(sqlUpdate)
            return self.id

    @staticmethod
    def updatePorGuildaEMundo(name, level, online, vocation, con):
        result = Character.select(name, con)
        sqlUpdate = "UPDATE Character SET level = ? , online = ? ,vocationId = ? WHERE id = ?".format(level, online,
                                                                                                      vocation,
                                                                                                      result[0][0])
        if len(result) == 0:
            return 0
        else:
            con.update(sqlUpdate)

    @staticmethod
    def updateNotificacaoMorte(idSelect, con):
        sqlUpdate = "UPDATE Character set ultimamortenotificada={}  WHERE id = {}".format(1, idSelect)
        con.update(sqlUpdate)

    @staticmethod
    def updatePorPlayer(name, level, online, vocation, guild, world, con, ultimaMorte, ultimaMorteMobOuPlayer,
                        ultimaMorteNotificada):
        if online:
            online = 1
        else:
            online = 0
        name = name.replace("'", "\\'")
        if ultimaMorteMobOuPlayer:
            ultimaMorteMobOuPlayer = 1
        else:
            ultimaMorteMobOuPlayer = 0
        result = Character.select(name, con)
        if len(result) == 0:
            return 0
        else:
            wor = World(world, con)
            worldID = wor.insert()
            guid = Guild(guild, world, con)
            guildID = guid.insert()
            voc = Vocation(vocation, con)
            voca = voc.insert()
            sqlUpdate = "UPDATE Character SET level = {} , online = {} ,vocationId = {}, guildId = {}, worldId = {}, ultimaMorte ='{}', ultimaMorteMobOuPlayer={}, ultimaMorteNotificada={} WHERE id = {}".format(
                level, online, voca, guildID, worldID, ultimaMorte, ultimaMorteMobOuPlayer, ultimaMorteNotificada,
                result[0][0])
            con.update(sqlUpdate)
