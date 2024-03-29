from BD.BD import BD
from BD.CharacterAmigos import CharacterAmigos
from BD.CharacterInimigos import CharacterInimigos
from BD.Guild import Guild
from BOT.funcoesBot import *


def iniciar(settings, semaforo):
    BDcon = BD(settings, settings["userBDAmigosInimigos"])
    while True:
        semaforo.acquire()
        tsconnEM = botsSecundarios(settings, "BotInimigos")
        tsconMorte = botsSecundarios(settings, "Mortes")

        inimigosOnline(tsconnEM, settings, tsconMorte, BDcon)
        tsconnEM.close()
        tsconnFD = botsSecundarios(settings, "BotAmigos")
        amigosOnline(tsconnFD, settings, tsconMorte, BDcon)
        tsconnFD.close()
        tsconMorte.close()

        semaforo.release()
        time.sleep(30)


def inimigosOnline(tsconn, settings, tsconMorte, BDcon):
    try:
        tsconn.send_keepalive()
        descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalInimigos"]))[0]["channel_description"]
        novaDescricao = "[table][tr][td]Nome[/td][td]Level[/td][td]Vocacao[/td][/tr]"
        resposta = CharacterInimigos.selectTodosInimigos(BDcon)
        totalInimigos = CharacterInimigos.selectQuantidadeInimigos(BDcon)
        if None is not resposta and None is not totalInimigos:
            contInimigosOnline = 0
            if resposta:
                for resp in resposta:
                    if(int(resp[9])==0):
                        notificaMorte(resp, "Inimigo Morreu: ", tsconMorte, BDcon)
                    contInimigosOnline += 1
                    vocacao=str(resp[4]).replace("_"," ").split()
                    if(len(vocacao)>1):
                        vocacao=vocacao[0][0]+""+vocacao[1][0]
                    else:
                        vocacao = vocacao[0][0]
                    novaDescricao += "[tr][td]" + resp[1] + "[/td][td]" + str(resp[2]) + "[/td][td]" + vocacao + "[/td][/tr]"
                novaDescricao += "[/table]"
                if descricao != novaDescricao:
                    nomeAtual = (
                        tsconn.channelinfo(cid=int(pegarIdChannel(tsconn, settings["canalInimigos"])))[0][
                            "channel_name"])
                    novoNome = settings["canalInimigos"] + " (" + str(contInimigosOnline) + "/" + str(
                        totalInimigos[0][0]) + ")"
                    if nomeAtual != novoNome:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalInimigos"]),
                                           channel_description=novaDescricao.strip(), channel_name=novoNome)
                    else:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalInimigos"]),
                                           channel_description=novaDescricao.strip())

                    # desativado poke inimigos
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


def amigosOnline(tsconn, settings, tsconMorte, BDcon):
    try:
        tsconn.send_keepalive()
        descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["canalAmigos"]))[0]["channel_description"]
        novaDescricao = "[table][tr][td]Nome[/td][td]Level[/td][/tr]"
        resposta = CharacterAmigos.selectTodosAmigos(BDcon)
        try:
            guildid = Guild.selectGuildID(BDcon, settings["nomeGuilda"])[0][0]
        except:
            guildid = 99999
        totalAmigos = CharacterAmigos.selectQuantidadeAmigosMenosGuilda(BDcon, guildid)
        todos = totalAmigos[0][0]
        if None is not resposta and None is not totalAmigos:
            contInimigosOnline = 0
            if resposta:
                for resp in resposta:
                    if resp[5] != settings["nomeGuilda"]:
                        if(int(resp[9])==0):
                            notificaMorte(resp, "Amigo Morreu: ", tsconMorte, BDcon)
                        contInimigosOnline += 1
                        novaDescricao += "[tr][td]" + resp[1] + "[/td][td]" + str(resp[2]) + "[/td][/tr]"
                    else:
                        if (resp[9] == 0):
                            notificaMorte(resp, "Membro Guilda Morreu: ", tsconMorte, BDcon)
                novaDescricao += "[/table]"
                if descricao != novaDescricao:
                    nomeAtual = (
                        tsconn.channelinfo(cid=int(pegarIdChannel(tsconn, settings["canalAmigos"])))[0]["channel_name"])
                    novoNome = settings["canalAmigos"] + " (" + str(contInimigosOnline) + "/" + str(todos) + ")"
                    if nomeAtual != novoNome:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalAmigos"]),
                                           channel_description=novaDescricao.strip(), channel_name=novoNome)
                    else:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalAmigos"]),
                                           channel_description=novaDescricao.strip())

                    # desativado poke amigos onlines
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
