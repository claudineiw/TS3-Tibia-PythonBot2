from BOT.funcoesBot import *
from Tibia import Events


class canalEventos:
    def __init__(self, settings, semaforo):
        self.settings = settings
        self.semaforo = semaforo
        self.eventos = Events.eventos()
        self.tsconn = botsSecundarios(self.settings, "BotEventos")

    def iniciar(self):
        ultimo = 0
        while (True):
            try:
                self.semaforo.acquire()
                if (self.tsconn.is_connected() == False):
                    self.tsconn = botsSecundarios(self.settings, "BotEventos")

                self.tsconn.send_keepalive()
                tsEvent = self.tsconn.wait_for_event(60)
                if ("reasonid" in tsEvent[0]):
                    if (int(tsEvent.parsed[0]["reasonid"]) == 0):
                        if (int(tsEvent.parsed[0]["client_type"]) == 0):
                            retorno = self.eventos.getEventsXPRespaw()
                            if (not retorno is None):
                                pokeCliente(retorno, int(tsEvent.parsed[0]["clid"]), self.tsconn)
                                enviarMensagem(retorno, int(tsEvent.parsed[0]["clid"]), self.tsconn)

                agora = time.time()
                if (agora - ultimo > 3600):
                    self.eventos.atualizaData()
                    self.AtualizaDescricaoCanal()
                    ultimo = time.time()

                self.semaforo.release()

            except Exception as e:
                if (not "Could not receive data from the server within the timeout" in e.__str__()):
                    print("Class CanalEventos.iniciar: " + e.__str__())
                    self.tsconn.close()
                    self.semaforo.release()
                pass

    def AtualizaDescricaoCanal(self):
        try:
            primeiro = False
            novaDescricao = "[table][tr][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][/tr][tr][/tr][tr]".format(
                "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo")
            for dia in self.eventos.getTodosEventos():
                if (primeiro == False):
                    for diasFaltantes in range(dia[0].value):
                        novaDescricao += "[td][/td]"
                    primeiro = True
                else:
                    if (dia[0].value == 0):
                        novaDescricao += "[tr][/tr][tr]"
                if (dia[0].value != 6):
                    novaDescricao += "[td]{}[/td]".format(
                        "[center][Color=Green](" + str(dia[1].day) + ")[/color]\n\n" + dia[2])
                else:
                    novaDescricao += "[td]{}[/td][/tr]".format(
                        "[center][Color=Green](" + str(dia[1].day) + ")[/color]\n\n" + dia[2])

            novaDescricao += "[/table]"

            descricao = self.tsconn.channelinfo(cid=pegarIdChannel(self.tsconn, self.settings["canalEventos"]))[0][
                "channel_description"]
            if novaDescricao != descricao:
                self.tsconn.channeledit(cid=pegarIdChannel(self.tsconn, self.settings["canalEventos"]),
                                        channel_description=novaDescricao)
        except:
            pass
