from BOT.funcoesBot import *
from pytz import timezone
import time
from datetime import datetime


def dreamCourts(settings):
    listaBosses=["Malofur","Maxxenius","Alptramun","Izcandar","Plagueroot"]
    contador=0
    diaDaSemanaAtual=0
    local=""
    while True:
        try:
            tz = timezone('Europe/Berlin')
            diaDaSemana = int(datetime.now(tz).isoweekday())
            if(diaDaSemanaAtual!=diaDaSemana):
                tsconn = botsSecundarios(settings,"DreamCourts")
                if(contador>4):
                    contador=0
                if diaDaSemana == 1:
                    local = listaBosses[contador]
                elif diaDaSemana == 2:
                    local = listaBosses[contador]
                elif diaDaSemana == 3:
                    local = listaBosses[contador]
                elif diaDaSemana == 4:
                    local = listaBosses[contador]
                elif diaDaSemana == 5:
                    local = listaBosses[contador]
                elif diaDaSemana == 6:
                    local = listaBosses[contador]
                elif diaDaSemana == 7:
                    local = listaBosses[contador]
                contador += 1
                diaDaSemanaAtual=diaDaSemana

                nomeCanal = settings["canalDreamCourts"]+" (" + local + ")"
                nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]))[0]["channel_name"]
                if nomeCanal != nomeAtual:
                    tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalDreamCourts"]), channel_name=nomeCanal)
                tsconn.close()
                time.sleep(1800)

        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, IndexError, ValueError,
                KeyError, TypeError):
            pass