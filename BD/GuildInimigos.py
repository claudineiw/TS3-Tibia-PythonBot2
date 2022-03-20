from BD.World import World


class GuildInimigos:
    def __init__(self, name, world, con):
        self.con = con
        if name is None:
            self.name = "None"
        else:
            self.name = name
        word = World(world, con)
        self.world = word.insert()
        self.id = 0

    def get(self):
        return self.id

    @staticmethod
    def select(con):
        sqlSelectTodosInimigos = "SELECT nome FROM GuildInimiga inner join Guild on guildId = Guild.id"
        return con.select(sqlSelectTodosInimigos)

    @staticmethod
    def selectId(name, con):
        sqlGuildId = "SELECT id FROM Guild where Guild.nome ILIKE '{}'".format(name)
        return con.select(sqlGuildId)

    @staticmethod
    def delete(guild, con):
        sqldeleteInimigo = "delete FROM GuildInimiga WHERE guildId ={} ".format(guild)
        return con.delete(sqldeleteInimigo)

    def insert(self):
        sqlInsertGuild = "INSERT INTO Guild (nome,worldId) VALUES('{}',{})".format(self.name, self.world)
        result = self.selectId(self.name, self.con)
        if len(result) == 0:
            self.id = self.con.insert(sqlInsertGuild)
            sqlInsertGuildInimiga = "INSERT INTO GuildInimiga (guildId) VALUES({})".format(self.id)
            self.con.insert(sqlInsertGuildInimiga)
            return True
        else:

            self.id = result[0][0]
            sqlSelectGuildInimiga = "select id from GuildInimiga where guildId={}".format(self.id)
            resultSelectGuilda = self.con.select(sqlSelectGuildInimiga)

            if len(resultSelectGuilda) != 0:
                return self.name + " guild ja esta na lista de inimigos"
            else:
                sqlInsertGuildInimiga = "INSERT INTO GuildInimiga (guildId) VALUES({})".format(self.id)
                self.con.insert(sqlInsertGuildInimiga)
                return True
