from BD.World import World
class Guild:
    def __init__(self, name, world,con):
        self.con=con
        if(name is None):
            self.name="None"
        else:
            self.name = name
        wor = World(world,con)
        self.world = wor.insert()
        self.id = 0
    def get(self):
        return self.id

    def select(self):
        sqlSelect = "SELECT id FROM Guild WHERE nome ILIKE '{}'".format(self.name)
        return self.con.select(sqlSelect)


    @staticmethod
    def selectGuildID(con,name):
        sqlSelect = "SELECT id FROM Guild WHERE nome ILIKE '{}'".format(name)
        return con.select(sqlSelect)


    def insert(self):
        result=self.select()
        if(len(result) == 0):
           sqlInsert = "INSERT INTO Guild (nome,worldId) VALUES('{}',{})".format(self.name,self.world)
           self.id=self.con.insert(sqlInsert)
           return self.id
        else:
            self.id=result[0][0]
            return self.id