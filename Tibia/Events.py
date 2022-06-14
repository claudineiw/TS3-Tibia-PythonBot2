import asyncio
import calendar
import datetime

import aiohttp
import tibiapy

from Auxiliares import agenda


class eventos:
    def __init__(self):
        self.now = None
        self.pegarDataAtual()
        self.eventos = asyncio.run(self.__getEventos__())

    def atualizaData(self):
        self.pegarDataAtual()
        self.eventos = asyncio.run(self.__getEventos__())

    def pegarDataAtual(self):
        self.now = datetime.datetime.now()
        # self.now = datetime.datetime(year=2021,month=11,day=5) #data teste

    async def __getEventos__(self):
        # url = tibiapy.EventSchedule.get_url(month=self.now.month, year=self.now.year)
        # r = requests.post(url)
        # content = r.text
        try:
            status=0
            url = tibiapy.EventSchedule.get_url(month=self.now.month, year=self.now.year)
            async with aiohttp.ClientSession() as session:
                while status != 200:
                    async with session.post(url) as resp:
                        status=resp.status
                        if (resp.status != 200):
                            continue
                        content = await resp.text()
            return tibiapy.EventSchedule.from_content(content)
        except:
           # pass
            print("")
            #self.__getEventos__()

    @property
    def getEventsXPRespaw(self):
        for evento in self.eventos.events:
            if (
                    evento.title == "Rapid Respawn" or evento.title == "XP/Skill Event" or "XP" in evento.title or "Skill Event" in evento.title):
                inicio = evento.start_date
                fim = evento.end_date
                if evento.start_date is None:
                    inicio = self.primeiroDiaDoMes()
                if evento.end_date is None:
                    fim = self.ultimoDiaDoMes()

                if inicio.month == self.now.month and fim.month == self.now.month:
                    if inicio.day <= self.now.day <= fim.day:
                        return "[Color=Purple]Esta rolando evento: " + evento.title + " comecou dia:" + inicio.day.__str__() + "/" + inicio.month.__str__() + " e vai ate: " + fim.day.__str__() + "/" + fim.month.__str__()

        return None

    def ultimoDiaDoMes(self):
        return self.now.replace(day=calendar.monthrange(self.now.year, self.now.month)[1]).date()

    def primeiroDiaDoMes(self):
        return datetime.date(year=self.now.year, month=self.now.month, day=1)

    def daterange(self, d1, d2):
        if d1 is None:
            d1 = self.primeiroDiaDoMes()
        if d2 is None:
            d2 = self.ultimoDiaDoMes()

        return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))

    def getTodosEventos(self):
        ag = agenda.agenda(self.now)
        for evento in self.eventos.events:
            for single_date in self.daterange(evento.start_date, evento.end_date):
                if single_date.month == self.now.month:
                    ag.agendar(single_date, evento.title)

        return ag.getAgenda()
