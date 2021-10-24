import tibiapy
import requests
import datetime
import calendar
from Auxiliares import agenda

CalendarioEvent=[]

def __getEventos__():
    now = datetime.datetime.now()
    url = tibiapy.EventSchedule.get_url(month=now.month, year=now.year)
    r = requests.post(url)
    content = r.text
    eventos = tibiapy.EventSchedule.from_content(content)
    return eventos,now

def getEventsXPRespaw():
    eventos,now=__getEventos__()
    for evento in eventos.events:
        if(evento.title=="Rapid Respawn" or evento.title=="XP/Skill Event" or "XP" in evento.title or "Skill Event" in evento.title):
            if(evento.start_date.month ==now.month):
                print(evento.start_date)
                print(evento.title)
                print(evento.end_date)


def ultimoDiaDoMes(now):
    return now.replace(day=calendar.monthrange(now.year,now.month)[1]).date()

def primeiroDiaDoMes(now):
    return datetime.date(year=now.year,month=now.month,day=1)

def daterange(d1, d2,now):
    if(d1 is None):
        d1=primeiroDiaDoMes(now)
    if(d2 is None):
        d2=ultimoDiaDoMes(now)

    return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))



def getTodosEventos():
    eventos, now = __getEventos__()
    ag=agenda.agenda(now)
    for evento in eventos.events:
            for single_date in daterange(evento.start_date, evento.end_date,now):
                if(single_date.month==now.month):
                    ag.agendar(single_date,evento.title)

    return ag.getAgenda()

