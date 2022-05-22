import asyncio

from Auxiliares import data
from BD.Character import Character as charBd
from Tibia import Character


class CharacterAmigos:
    def __init__(self, name, con):
        self.con = con
        if name is None:
            self.name = "None"
        else:
            self.name = name
        self.id = 0

    def get(self):
        return self.id

    @staticmethod
    def select(con):
        sqlSelectTodosAmigos = "SELECT Character.nome FROM CharacterAmigo inner join Character on characterId=Character.id"
        return con.select(sqlSelectTodosAmigos)

    @staticmethod
    def selectTodosAmigos(con):
        sqlSelect = '''SELECT Character.id,Character.nome,level,online,Vocations.nome,Guild.nome,World.nome,Character.ultimaMorte ,Character.ultimaMorteMobOuPlayer ,Character.ultimaMorteNotificada 
                    FROM Character 
                    inner join world on(character.worldid=world.id)
                    inner join Guild on Character.guildid=Guild.id 
                    inner join vocations on (character.vocationid=vocations.id)
                    where  online=1 and (Guild.id in (select guildid from guildamiga) or Character.id in (SELECT characterid FROM public.CharacterAmigo ))
                    order by character.nome'''
        return con.select(sqlSelect)

    @staticmethod
    def selectQuantidadeAmigos(con):
        sqlSelect = '''SELECT count(Character.id) 
                        FROM Character 
                        inner join world on(character.worldid=world.id)
                        inner join Guild on Character.guildid=Guild.id 
                        inner join vocations on (character.vocationid=vocations.id)
                        where  Guild.id in (select guildid from guildamiga) or Character.id in (SELECT characterid FROM public.CharacterAmigo )'''
        return con.select(sqlSelect)

    @staticmethod
    def selectQuantidadeAmigosMenosGuilda(con, guilda):
        sqlSelect = '''SELECT count(Character.id) 
                           FROM Character 
                           inner join world on(character.worldid=world.id)
                           inner join Guild on Character.guildid=Guild.id 
                           inner join vocations on (character.vocationid=vocations.id)
                           where Character.guildid!={} and Guild.id in (select guildid from guildamiga) or Character.id in (SELECT characterid FROM public.CharacterAmigo )'''.format(
            guilda)
        return con.select(sqlSelect)

    @staticmethod
    def delete(character, con):
        sqldeleteAmigos = "delete FROM CharacterAmigo WHERE characterId ={}".format(character)
        return con.delete(sqldeleteAmigos)

    def insert(self):
        resultSelect = charBd.select(self.name, self.con)
        if len(resultSelect) == 0:
            char = asyncio.run(Character.get_character(self.name))
            if char is None:
                return self.name + " personagem nao encontrado"
            else:
                if len(char.deaths) > 0:
                    dataMorteAtual = data.utc_to_local(char.deaths[0].time)
                    addCharBd = charBd(char.name, char.level, 0, char.world, char.guild_name, char.vocation.name,
                                       dataMorteAtual, char.deaths[0].by_player, 1, self.con)
                else:
                    addCharBd = charBd(char.name, char.level, 0, char.world, char.guild_name, char.vocation.name,
                                       "0", 0, 1, self.con)
                self.id = addCharBd.insert()

                sqlInsertInimigo = "INSERT INTO CharacterAmigo (characterId) VALUES({})".format(self.id)
                self.con.insert(sqlInsertInimigo)
                return True
        else:
            self.id = resultSelect[0][0]
            sqlSelectInimigo = "SELECT id FROM CharacterAmigo WHERE characterId ={}".format(self.id)
            resultSelectInimigo = self.con.select(sqlSelectInimigo)
            if len(resultSelectInimigo) > 0:
                return self.name + " Ja esta inserido em amigos"
            else:
                sqlInsertInimigo = "INSERT INTO CharacterAmigo (characterId) VALUES({})".format(self.id)
                self.con.insert(sqlInsertInimigo)
                return True
