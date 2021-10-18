from BD.World import World
class GuildAmigos:
    def __init__(self, name, world,con):
        self.con=con
        if(name is None):
            self.name="None"
        else:
            self.name = name
        word = World(world,con)
        self.world = word.insert()
        self.id = 0

    def get(self):
        return self.id

    @staticmethod
    def select(con):
        sqlSelectTodosAmigos = "SELECT nome FROM GuildAmiga inner join Guild on guildId = Guild.id"
        return con.select(sqlSelectTodosAmigos)

    @staticmethod
    def selectId(name,con):
        sqlGuildId = "SELECT id FROM Guild where  Guild.nome ILIKE '{}'".format(name)
        return con.select(sqlGuildId)

    @staticmethod
    def delete(guild, con):
        sqldeleteAmigo = "delete FROM GuildAmiga WHERE guildId ={} ".format(guild)
        return con.delete(sqldeleteAmigo)

    def insert(self):
        sqlInsertGuild = "INSERT INTO Guild (nome,worldId) VALUES('{}',{})".format(self.name,self.world)
        result = self.selectId(self.name,self.con)
        if(len(result) == 0):
           self.id=self.con.insert(sqlInsertGuild)
           sqlInsertGuildAmiga = "INSERT INTO GuildAmiga (guildId) VALUES({})".format(self.id)
           self.con.insert(sqlInsertGuildAmiga)
           return True
        else:
            self.id = result[0][0]
            sqlSelectGuildAmiga = "select id from GuildAmiga where guildId={}".format(self.id)
            resultSelectGuilda = self.con.select(sqlSelectGuildAmiga)

            if (len(resultSelectGuilda)!=0):
                return self.name + " guild ja esta na lista de amigos"
            else:
                sqlInsertGuildAmiga = "INSERT INTO GuildAmiga (guildId) VALUES({})".format(self.id)
                self.con.insert(sqlInsertGuildAmiga)
                return True