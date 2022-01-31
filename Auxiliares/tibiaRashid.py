from BOT.funcoesBot import *
from pytz import timezone
import time
from datetime import datetime
def rashidCidade(settings):
    while True:

        try:
            tz = timezone('Europe/Berlin')
            diaDaSemana = int(datetime.now(tz).isoweekday())
            tsconn = botsSecundarios(settings,"Rashid")
            descricaoAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalRashid"]))[0]["channel_description"]
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
            novaDescricao = ""
            for linhas in descricaoAtual.split("\n"):
                if linhas.find("Local") != -1:
                    novaDescricao += ondeFica + "\n"
                else:
                    novaDescricao += linhas + "\n"

            nomeCanal = settings["canalRashid"]+" (" + local + ")"
            nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalRashid"]))[0]["channel_name"]
            if nomeCanal != nomeAtual:
                tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalRashid"]), channel_name=nomeCanal, channel_description=novaDescricao)
            tsconn.close()
            time.sleep(1800)

        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, IndexError, ValueError,
                KeyError, TypeError):
            pass