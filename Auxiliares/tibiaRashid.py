import time
from datetime import datetime

from pytz import timezone

from BOT.funcoesBot import *


def rashidCidade(settings, semaforo):
    while True:
        semaforo.acquire()
        tsconn = botsSecundarios(settings, "Rashid")
        try:
            tz = timezone('Europe/Berlin')
            diaDaSemana = int(datetime.now(tz).isoweekday())
            ondeFica = ""
            local = ""
            hora = int(datetime.now(tz).time().hour)
            minuto = int(datetime.now(tz).time().minute)
            if (hora >= 10):
                if diaDaSemana == 1:
                    local = "Svargrond"
                    ondeFica = "[b]Local[/b]: Nas segundas você pode encontrá-lo em Svargrond, na taverna de Dankwart, ao sul do templo"
                elif diaDaSemana == 2:
                    local = "Liberty Bay"
                    ondeFica = "[b]Local[/b]: Nas terças você pode encontrá-lo em Liberty Bay, na taverna de Lyonel ao oeste do depot"
                elif diaDaSemana == 3:
                    local = "Port Hope"
                    ondeFica = "[b]Local[/b]: Nas quartas você pode encontrá-lo em Port Hope, na taverna de Clyde ao norte do barco"
                elif diaDaSemana == 4:
                    local = "Ankrahmun"
                    ondeFica = "[b]Local[/b]: Nas quintas você pode encontrá-lo em Ankrahmun, na taverna de Arito, acima do post office"
                elif diaDaSemana == 5:
                    local = "Darashia"
                    ondeFica = "[b]Local[/b]: Nas sextas você pode encontrá-lo em Darashia, na taverna de Miraia, a oeste do barco"
                elif diaDaSemana == 6:
                    local = "Edron"
                    ondeFica = "[b]Local[/b]: Nos sábados você pode encontrá-lo em Edron, na taverna de Mirabell, acima do depot"
                elif diaDaSemana == 7:
                    local = "Carlin"
                    ondeFica = "[b]Local[/b]: Nos domingos você pode encontrá-lo no primeiro andar do depot de Carlin"

                nomeCanal = settings["canalRashid"] + " (" + local + ")"
                nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalRashid"]))[0]["channel_name"]
                if nomeCanal != nomeAtual:
                    tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalRashid"]), channel_name=nomeCanal,
                                       channel_description=ondeFica)

            tsconn.close()
            semaforo.release()
            time.sleep(3600)

        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, IndexError, ValueError,
                KeyError, TypeError):
            tsconn.close()
            semaforo.release()
            pass
