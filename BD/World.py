class World:
    def __init__(self, name,con):
        self.con=con
        self.name = name
        self.id = 0

    def get(self):
        return self.id


    def select(self):
        sqlSelect = "SELECT id FROM World WHERE nome ILIKE '{}'".format(self.name)
        return self.con.select(sqlSelect)

    def insert(self):
        if(type(self.name) == type(1)):
            return self.name
        result = self.select()
        if(len(result) == 0):
           sqlInsert = "INSERT INTO World (nome) VALUES('{}')".format(self.name)
           self.id=self.con.insert(sqlInsert)
           return self.id
        else:
            self.id=result[0][0]
            return self.id