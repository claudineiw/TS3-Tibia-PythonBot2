import ts3 as ts3

from BOT.funcoesBot import *
from pytz import timezone
import time
from datetime import datetime


def dreamCourts(settings,semaforo):
    listaBosses=["Alptramun","Izcandar","Plagueroot","Malofur","Maxxenius"]
    contador=0
    local=""

    while True:
        try:
            semaforo.acquire()
            arquivo = open('dia.txt', 'r')
            diaDaSemanaAtual = int(arquivo.read())
            arquivo.close()

            tz = timezone('Europe/Berlin')
            diaDaSemana = int(datetime.now(tz).isoweekday())
            hora = int(datetime.now(tz).time().hour)
            if(hora>=10):
                if(diaDaSemanaAtual!=diaDaSemana):
                    print(diaDaSemana)
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
                    arquivo = open('dia.txt', 'w')
                    arquivo.write(str(diaDaSemana))
                    arquivo.close()

                    nomeCanal = settings["canalDreamCourts"]+" (" + local + ")"
                    nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]))[0]["channel_name"]
                    if nomeCanal != nomeAtual:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalDreamCourts"]), channel_name=nomeCanal)
                    tsconn.close()

            semaforo.release()
            time.sleep(3600)

        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, IndexError, ValueError,
                KeyError, TypeError):
            pass