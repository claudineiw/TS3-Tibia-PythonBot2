class Vocation:
    def __init__(self, name, con):
        self.con = con
        self.name = "None"
        if name is None:
            self.name = "None"
        elif name == "Elite Knight":
            self.name = "ELITE_KNIGHT"
        elif name == "Elder Druid":
            self.name = "ELDER_DRUID"
        elif name == "Master Sorcerer":
            self.name = "MASTER_SORCERER"
        elif name == "Royal Paladin":
            self.name = "ROYAL_PALADIN"
        elif name == "Knight":
            self.name = "KNIGHT"
        elif name == "Druid":
            self.name = "DRUID"
        elif name == "Sorcerer":
            self.name = "SORCERER"
        elif name == "Paladin":
            self.name = "PALADIN"
        else:
            self.name = name
        self.id = 0

    def get(self):
        return self.id

    def select(self):
        sqlSelect = "SELECT id FROM Vocations WHERE  nome = '{}'".format(self.name)
        return self.con.select(sqlSelect)

    def insert(self):
        result = self.select()
        if len(result) == 0:
            sqlInsert = "INSERT INTO Vocations (nome) VALUES('{}')".format(self.name)
            self.id = self.con.insert(sqlInsert)
            return self.id
        else:
            self.id = result[0][0]
            return self.id
