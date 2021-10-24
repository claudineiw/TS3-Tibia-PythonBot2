from BOT.funcoesBot import *
from Tibia import Events
class canalEventos:
    def __init__(self,settings):
        self.settings=settings

    def iniciar(self):
        try:
            while(True):
                tsconn = botsSecundarios(self.settings, "BotEventos")
                eventos = Events.getTodosEventos()
                primeiro=False
                tsconn.send_keepalive()
                novaDescricao = "[table][tr][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][td][center]{}[/td][/tr][tr][/tr][tr]".format("Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo")

                for dia in eventos:
                    if(primeiro==False):
                        for diasFaltantes in range(dia[0].value):
                            novaDescricao+="[td][/td]"
                        primeiro=True
                    else:
                        if(dia[0].value==0):
                            novaDescricao+="[tr][/tr][tr]"
                    if(dia[0].value!=6):
                        novaDescricao+="[td]{}[/td]".format("[center][Color=Green]("+str(dia[1].day)+")[/color]\n\n"+dia[2])
                    else:
                        novaDescricao+="[td]{}[/td][/tr]".format("[center][Color=Green]("+str(dia[1].day)+")[/color]\n\n"+dia[2])


                novaDescricao+="[/table]"

                descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn, self.settings["canalEventos"]))[0][
                    "channel_description"]
                if novaDescricao != descricao:
                    tsconn.channeledit(cid=pegarIdChannel(tsconn, self.settings["canalEventos"]),
                                       channel_description=novaDescricao)
                tsconn.close()
                time.sleep(3600)





        except:
            pass


