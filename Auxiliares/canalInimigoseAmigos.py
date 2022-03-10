from BOT.funcoesBot import *
from BD.BD import BD
from BD.CharacterInimigos import CharacterInimigos
from BD.CharacterAmigos import CharacterAmigos
from BD.Guild import Guild
def iniciar(settings,semaforo):
    BDcon = BD(settings,settings["userBDAmigosInimigos"])
    while(True):
        semaforo.acquire()
        tsconnEM = botsSecundarios(settings, "BotInimigos")
        tsconMorte = botsSecundarios(settings, "Mortes")

        inimigosOnline(tsconnEM,settings,tsconMorte,BDcon)
        tsconnEM.close()
        tsconnFD = botsSecundarios(settings, "BotAmigos")
        amigosOnline(tsconnFD,settings,tsconMorte,BDcon)
        tsconnFD.close()
        tsconMorte.close()


        semaforo.release()
        time.sleep(30)


def inimigosOnline(tsconn,settings,tsconMorte,BDcon):
        try:
            tsconn.send_keepalive()
            descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn,settings["canalInimigos"]))[0]["channel_description"]
            novaDescricao = "[table][tr][td]Nome[/td][td]Level[/td][/tr]"
            resposta = CharacterInimigos.selectTodosInimigos(BDcon)
            totalInimigos = CharacterInimigos.selectQuantidadeInimigos(BDcon)
            if not type(resposta) is type(None) and not type(totalInimigos) is type(None):
                contInimigosOnline = 0
                if resposta != False:
                    for resp in resposta:
                        notificaMorte(resp,"Inimigo Morreu: ",tsconMorte,BDcon)
                        contInimigosOnline += 1
                        novaDescricao += "[tr][td]" + resp[1] + "[/td][td]" + str(resp[2]) + "[/td][/tr]"
                    novaDescricao += "[/table]"
                    if descricao != novaDescricao:
                        nomeAtual = (
                            tsconn.channelinfo(cid=int(pegarIdChannel(tsconn,settings["canalInimigos"])))[0][
                                "channel_name"])
                        novoNome = settings["canalInimigos"] + " (" + str(contInimigosOnline) + "/" + str(totalInimigos[0][0]) + ")"
                        if nomeAtual != novoNome:
                            tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalInimigos"]),
                                               channel_description=novaDescricao.strip(), channel_name=novoNome)
                        else:
                            tsconn.channeledit(cid=pegarIdChannel(tsconn,settings["canalInimigos"]),
                                               channel_description=novaDescricao.strip())

                        #desativado poke inimigos
                        ''' novaDescricao = novaDescricao.replace("[table][td]Nome[/td][td]Level[/td][/tr]",
                                                              "").replace("[/table]", "")
                        descricao = descricao.replace("[table][td]Nome[/td][td]Level[/td][/tr]", "").replace(
                            "[/table]", "")
                        for itens in descricao.split("[tr]"):
                            novaDescricao = novaDescricao.replace(itens, "")

                        for itens in novaDescricao.split("[tr]"):
                            atual = itens[itens.find("[td]") + 4:itens.find("[/td]")].strip().rstrip()
                            if atual != "":
                                pokeTodosClientes("[COLOR=red]Inimigo online: " + atual,tsconn)'''


        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError):
            pass


def amigosOnline(tsconn, settings,tsconMorte, BDcon):
    try:
        tsconn.send_keepalive()
        descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalAmigos"]))[0]["channel_description"]
        novaDescricao = "[table][tr][td]Nome[/td][td]Level[/td][/tr]"
        resposta = CharacterAmigos.selectTodosAmigos(BDcon)
        try:
            guildid=Guild.selectGuildID(BDcon,settings["nomeGuilda"])[0][0]
        except:
            guildid=99999
        totalAmigos = CharacterAmigos.selectQuantidadeAmigosMenosGuilda(BDcon,guildid)
        todos=totalAmigos[0][0]
        if not type(resposta) is type(None) and not type(totalAmigos) is type(None):
            contInimigosOnline = 0
            if resposta != False:
                for resp in resposta:
                    if(resp[5]!=settings["nomeGuilda"]):
                        notificaMorte(resp, "Amigo Morreu: ", tsconMorte, BDcon)
                        contInimigosOnline += 1
                        novaDescricao += "[tr][td]" + resp[1] + "[/td][td]" + str(resp[2]) + "[/td][/tr]"
                    else:
                        notificaMorte(resp, "Membro Guilda Morreu: ", tsconMorte, BDcon)
                novaDescricao += "[/table]"
                if descricao != novaDescricao:
                        nomeAtual = (tsconn.channelinfo(cid=int(pegarIdChannel(tsconn, settings["canalAmigos"])))[0]["channel_name"])
                        novoNome = settings["canalAmigos"] + " (" + str(contInimigosOnline) + "/" + str(todos) + ")"
                        if nomeAtual != novoNome:
                            tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalAmigos"]),
                                               channel_description=novaDescricao.strip(), channel_name=novoNome)
                        else:
                            tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalAmigos"]),
                                               channel_description=novaDescricao.strip())


                        #desativado poke amigos onlines
                        '''novaDescricao = novaDescricao.replace("[table][td]Nome[/td][td]Level[/td][/tr]",
                                                              "").replace("[/table]", "")
                        descricao = descricao.replace("[table][td]Nome[/td][td]Level[/td][/tr]", "").replace(
                            "[/table]", "")
                        for itens in descricao.split("[tr]"):
                            novaDescricao = novaDescricao.replace(itens, "")

                        for itens in novaDescricao.split("[tr]"):
                            atual = itens[itens.find("[td]") + 4:itens.find("[/td]")].strip().rstrip()
                            if atual != "":
                                pokeTodosClientes("[COLOR=blue]Amigo online: " + atual, tsconn)'''

    except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError):
        pass