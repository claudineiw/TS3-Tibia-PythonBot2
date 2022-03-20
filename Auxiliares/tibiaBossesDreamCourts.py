from pytz import timezone

from BOT.funcoesBot import *


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class ListaDreamCourtsCircular:
    def __init__(self):
        self.head = None
        self.addBoss("Izcandar")
        self.addBoss("Alptramun")
        self.addBoss("Maxxenius")
        self.addBoss("Malofur")
        self.addBoss("Plagueroot")
        self.irParaProximo = False

    def addBoss(self, data):
        ptr_1 = Node(data)
        temp = self.head
        ptr_1.next = self.head

        if self.head is not None:
            while temp.next != self.head:
                temp = temp.next
            temp.next = ptr_1
        else:
            ptr_1.next = ptr_1
        self.head = ptr_1

    def cabeca(self):
        return self.head

    def next(self):
        self.irParaProximo = True

    def irParaParaFrente(self):
        if self.irParaProximo == False:
            return False
        else:
            self.irParaProximo = False
            return True


def dreamCourts(settings, semaforo, classBoss):
    lista = classBoss.cabeca()
    tsconn = botsSecundarios(settings, "DreamCourts")
    nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]))[0]["channel_name"]
    if not lista.data in nomeAtual:
        while True:
            lista = lista.next
            if lista.data in nomeAtual:
                break
    tsconn.close()

    while True:
        semaforo.acquire()
        try:
            tsconn = botsSecundarios(settings, "DreamCourts")
            arquivo = open('dia.txt', 'r')
            diaDaSemanaAtual = int(arquivo.read())
            arquivo.close()

            tz = timezone('Europe/Berlin')
            diaDaSemana = int(datetime.now(tz).isoweekday())
            hora = int(datetime.now(tz).time().hour)
            nomeAtual = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]))[0]["channel_name"]

            if hora >= 10:
                if diaDaSemanaAtual != diaDaSemana:
                    arquivo = open('dia.txt', 'w')
                    arquivo.write(str(diaDaSemana))
                    arquivo.close()
                    lista = lista.next
                    nomeCanal = settings["canalDreamCourts"] + " (" + lista.data + ")"
                    if nomeCanal != nomeAtual:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]),
                                           channel_name=nomeCanal)

            if classBoss.irParaParaFrente():
                lista = lista.next
                nomeCanal = settings["canalDreamCourts"] + " (" + lista.data + ")"
                if nomeCanal != nomeAtual:
                    tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalDreamCourts"]), channel_name=nomeCanal)

            tsconn.close()
            semaforo.release()
            time.sleep(30)

        except:
            # tsconn.close()
            semaforo.release()
            pass
