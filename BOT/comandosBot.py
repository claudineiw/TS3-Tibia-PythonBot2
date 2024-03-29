from __future__ import absolute_import

import threading
from datetime import timedelta, datetime

import BOT.AmigosEnimigos as AmigosEInimigos
import BOT.funcoesBot as funcoesBot
import BOT.funcoesGerais as funGeral
import BOT.listaHelp as listaHelp
from Auxiliares import tibiaHunt
from BD.usuarioTS import usuarioTS


def botBoasVindas(nomeUsuario, usuarioID, bot):
    try:
        funcoesBot.enviarMensagem("\nBem vindo " + nomeUsuario + "\nPara ver comandos digite !help", usuarioID, bot)
    except Exception as e:
        print("botBoasVindas "+e.__str__())
        return None


def botHelp(usuarioID, bot, settings):
    try:
        lista = listaHelp.listaHelp(funcoesBot.pegarPermissoesCliente(usuarioID, bot), settings)
        for item in lista:
            funcoesBot.enviarMensagem(item, usuarioID, bot)
    except Exception as e:
        print("botHelp "+e.__str__())
        return None


def botShared(mensagemRecebida, nomeUsuario, usuarioID, bot):
    try:
        level = int(mensagemRecebida.split()[1])
        mensagem = funGeral.calculoShared(level, nomeUsuario)
        funcoesBot.enviarMensagem(mensagem, usuarioID, bot)
    except Exception as e:
        print("botShared " + e.__str__())
        funcoesBot.enviarMensagem("\nErro de parametro favor informar como no exemplo !shared <100>", usuarioID, bot)


def botloot(mensagemRecebida, usuarioID, bot):
    try:
        mensagem = mensagemRecebida.replace("!hunt ", "")
        hunt = tibiaHunt.tibiaHunt(mensagem)
        result = hunt.getResult()
        for x in range(len(result)):
            funcoesBot.enviarMensagem(result[x], usuarioID, bot)
    except Exception as e:
        print("botloot " + e.__str__())
        funcoesBot.enviarMensagem("\nErro de parametro favor informar como no exemplo !loot dados", usuarioID, bot)
        return None


def botMassPokeBoss(nome, mensagemRecebida, settings):
    try:
        mensagem = mensagemRecebida.replace("!boss ", "")
        threading.Thread(name="PokeBoss", target=funcoesBot.pokerTodosClientesBoss,
                         args=(settings, mensagem, funcoesBot.botsSecundarios(settings, "Boss-" + nome),)).start()
    except Exception as e:
        print("botMassPokeBoss " + e.__str__())
        return None


def botMassPokeVendas(nome, mensagemRecebida, settings):
    try:
        mensagem = mensagemRecebida.replace("!sell ", "")
        threading.Thread(name="PokeVendas", target=funcoesBot.pokerTodosClientesVendas,
                         args=(settings, mensagem, funcoesBot.botsSecundarios(settings, "Vendas-" + nome),)).start()
    except Exception as e:
        print("botMassPokeVendas " + e.__str__())
        return None


def botMassPoke(nome, mensagemRecebida, settings):
    try:
        mensagem = mensagemRecebida.replace("!mp ", "")
        threading.Thread(name="Poke", target=funcoesBot.pokeTodosClientes,
                         args=(mensagem, funcoesBot.botsSecundarios(settings, "BOT-" + nome),)).start()
    except Exception as e:
        print("botMassPoke " + e.__str__())
        return None


def botMvCh(stringCanais, idUsuario, bot):
    try:
        stringCanais = stringCanais.replace("!mvch ", "")
        canalOrigem, canalDestino = funcoesBot.trataCanaisComEspaco(stringCanais, bot)
        if None is not canalOrigem:
            if None is not canalDestino:
                for cliente in funcoesBot.pegarListaClientes(bot):
                    if int(cliente["client_type"]) != 1:
                        if int(cliente["cid"]) == int(funcoesBot.pegarIdChannel(bot, canalOrigem)):
                            bot.clientmove(cid=funcoesBot.pegarIdChannel(bot, canalDestino), clid=cliente["clid"])

            else:
                funcoesBot.enviarMensagem("Canal de destino incorreto", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("Canal de origem incorreto", idUsuario, bot)


    except Exception as e:
        print("botMvCh " + e.__str__())
        funcoesBot.enviarMensagem("Erro nome dos canais favor verificar", idUsuario, bot)
        return None


def botBossDreamCourtsNext(idUsuario, bot, listaBossesDreamCourts):
    try:
        listaBossesDreamCourts.next()
        funcoesBot.enviarMensagem("Proximo Boss", idUsuario, bot)
    except Exception as e:
        print("botBossDreamCourtsNext " + e.__str__())
        funcoesBot.enviarMensagem("Erro ao trocar boss", idUsuario, bot)
        return None


def botMvTodosParaMim(idUsuario, bot):
    try:
        canalDestino = ""
        for cliente in funcoesBot.pegarListaClientes(bot):
            if int(cliente["clid"]) == int(idUsuario):
                canalDestino = cliente["cid"]
                break
        for cliente in funcoesBot.pegarListaClientes(bot):
            if int(cliente["client_type"]) != 1:
                if int(cliente["cid"]) != int(canalDestino):
                    bot.clientmove(cid=canalDestino, clid=cliente["clid"])

    except Exception as e:
        print("botMvTodosParaMim " + e.__str__())
        funcoesBot.enviarMensagem("Erro nome dos canais favor verificar", idUsuario, bot)
        return None


def botAddFd(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!addfd ", "")
        amigos = AmigosEInimigos.AmigosEnimigos()
        retorno = amigos.addCharacterAmigo(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " adicionado aos amigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botAddFd "+e.__str__())
        return None


def botRmFd(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmfd ", "")
        amigos = AmigosEInimigos.AmigosEnimigos()
        retorno = amigos.deleteCharacterAmigos(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " removido dos amigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botRmFd "+e.__str__())
        return None


def botAfkTrocaTempo(mensagemRecebida, tempo, idUsuario, bot):
    mensagemRecebida = mensagemRecebida.replace("!afk ", "")
    try:
        tempo.setTempo(int(mensagemRecebida))
        funcoesBot.enviarMensagem("Tempo do AFK foi alterado", idUsuario, bot)
    except Exception as e:
        print("botAfkTrocaTempo " + e.__str__())
        funcoesBot.enviarMensagem("Erro no parametro", idUsuario, bot)
        return None


def botAddEm(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!addem ", "")
        inimigo = AmigosEInimigos.AmigosEnimigos()
        retorno = inimigo.addCharacterInimigo(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " adicionado aos inimigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botAddEm "+e.__str__())
        return None


def botRmEm(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmem ", "")
        inimigo = AmigosEInimigos.AmigosEnimigos()
        retorno = inimigo.deleteCharacterInimigos(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " removido dos inimigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botRmEm "+e.__str__())
        return None


def botLtEm(con, idUsuario, bot):
    try:
        inimigo = AmigosEInimigos.AmigosEnimigos()
        personagensInimigos = inimigo.selectCharacterInimigos(con)
        guildasInimigas = inimigo.selectGuildInimigas(con)

        if len(personagensInimigos) != 0:
            funcoesBot.enviarMensagem("<------Personagens Inimigos------->", idUsuario, bot)
            for personagem in personagensInimigos:
                funcoesBot.enviarMensagem(personagem, idUsuario, bot)

            funcoesBot.enviarMensagem("<------Fim Personagens Inimigos------->", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("Nao ha personagens inimigos adicionados", idUsuario, bot)

        if len(guildasInimigas) != 0:
            funcoesBot.enviarMensagem("<------Guildas Inimigas------->", idUsuario, bot)
            for guilda in guildasInimigas:
                funcoesBot.enviarMensagem(guilda, idUsuario, bot)
            funcoesBot.enviarMensagem("<------Fim Guildas Inimigas------->", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("Nao ha guildas inimigas adicionadas", idUsuario, bot)
    except Exception as e:
        print("botLtEm "+e.__str__())
        return None


def botLtfd(con, idUsuario, bot):
    try:
        amigos = AmigosEInimigos.AmigosEnimigos()
        personagensAmigos = amigos.selectCharacterAmigos(con)
        guildasAmigas = amigos.selectGuildAmigas(con)

        if len(personagensAmigos) != 0:
            funcoesBot.enviarMensagem("<------Personagens Amigos------->", idUsuario, bot)
            for personagem in personagensAmigos:
                funcoesBot.enviarMensagem(personagem, idUsuario, bot)

            funcoesBot.enviarMensagem("<------Fim Personagens Amigos------->", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("Nao ha personagens amigos adicionados", idUsuario, bot)

        if len(guildasAmigas) != 0:
            funcoesBot.enviarMensagem("<------Guildas Amigas------->", idUsuario, bot)
            for guilda in guildasAmigas:
                funcoesBot.enviarMensagem(guilda, idUsuario, bot)
            funcoesBot.enviarMensagem("<------Fim Guildas Amigas------->", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("Nao ha guildas amigas adicionadas", idUsuario, bot)
    except Exception as e:
        print("botLtfd "+e.__str__())
        return None


def botLtuser(con, idUsuario, bot):
    try:
        usuariosTS = usuarioTS.select(con)
        if len(usuariosTS) != 0:
            funcoesBot.enviarMensagem("<------Lista Usuarios------->", idUsuario, bot)
            for userTS in usuariosTS:
                userMain = usuarioTS.selectUsuario(userTS[0], con)
                uid = userMain[0][5]
                dbID = funcoesBot.pegarDBIDfromUID(uid, bot)["cldbid"]
                ultimoLogin = datetime.fromtimestamp(int(bot.clientdbinfo(cldbid=dbID)[0]["client_lastconnected"]))
                seteDiasAtras = datetime.now() - timedelta(7)
                if ultimoLogin < seteDiasAtras:
                    funcoesBot.enviarMensagem(
                        "[color=red]{}{}\t{}{}\t{}{}\tUltimo Login: {}[/color]".format(userMain[0][0], userMain[0][1],
                                                                                       userMain[0][2], userMain[0][3],
                                                                                       userMain[0][4], userMain[0][5],
                                                                                       ultimoLogin), idUsuario, bot)
                else:
                    funcoesBot.enviarMensagem(
                        "{}{}\t{}{}\t{}{}\tUltimo Login: {}".format(userMain[0][0], userMain[0][1], userMain[0][2],
                                                                    userMain[0][3], userMain[0][4], userMain[0][5],
                                                                    ultimoLogin), idUsuario, bot)
                if not userTS[3] is None:
                    if len(userTS[3]) > 0:
                        for maker in userTS[3]:
                            makerDescricao = usuarioTS.selectMaker(maker, userTS[2], con)
                            funcoesBot.enviarMensagem(
                                "\t\t\t\t{}{}\t{}{}".format(makerDescricao[0][0], makerDescricao[0][1],
                                                            makerDescricao[0][2], makerDescricao[0][3]), idUsuario, bot)
                    else:
                        funcoesBot.enviarMensagem("\t\t\t\t<------Nao tem Maker------>", idUsuario, bot)
                else:
                    funcoesBot.enviarMensagem("\t\t\t\t<------Nao tem Maker------>", idUsuario, bot)

            funcoesBot.enviarMensagem("<------Fim Lista Usuarios------->", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem("<------Nenhum usuario encontrado------->", idUsuario, bot)
    except Exception as e:
        print("botLtuser "+e.__str__())
        return None


def botAddFdgui(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!addfdgui ", "")
        amigos = AmigosEInimigos.AmigosEnimigos()
        retorno = amigos.addGuildAmiga(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " adicionado aos amigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botAddFdgui "+e.__str__())
        return None


def botRmFdgui(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmfdgui ", "")
        inimigo = AmigosEInimigos.AmigosEnimigos()
        retorno = inimigo.deleteGuildAmigas(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " removido dos amigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botRmFdgui "+e.__str__())
        return None


def botAddEmgui(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!addemgui ", "")
        inimigos = AmigosEInimigos.AmigosEnimigos()
        retorno = inimigos.addGuildInimiga(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " adicionado aos inimigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botAddEmgui "+e.__str__())
        return None


def botRmEmgui(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmemgui ", "")
        inimigo = AmigosEInimigos.AmigosEnimigos()
        retorno = inimigo.deleteGuildInimigas(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " removido de inimigos", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botRmEmgui "+e.__str__())
        return None


def botaddUserTS(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!adduser ", "")
        nomeMain, nomeTS, usuarioUID = funcoesBot.pegarNomeEUsuario(mensagemRecebida, bot)
        if usuarioUID is None:
            funcoesBot.enviarMensagem("Usuario nao encontrado", idUsuario, bot)
        else:
            usuarioTSs = usuarioTS(nomeTS, nomeMain, usuarioUID, con)
            retorno = usuarioTSs.insert()
            if retorno:
                funcoesBot.enviarMensagem(nomeTS + " adicionado aos Usuarios personagem Main: " + nomeMain, idUsuario, bot)
            else:
                funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botaddUserTS "+e.__str__())
        return None


def botrmUserTS(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmuser ", "")
        retorno = usuarioTS.deletePorCharacterMain(mensagemRecebida, con)
        if retorno:
            funcoesBot.enviarMensagem(mensagemRecebida + " removido de usuarios ", idUsuario, bot)
        else:
            funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botrmUserTS "+e.__str__())
        return None


def botaddMakerUserTS(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!addmaker ", "")
        nomeMain, nomeMaker = funcoesBot.pegarNomeMainEMaker(mensagemRecebida, con)
        if nomeMain is None:
            funcoesBot.enviarMensagem(
                "main nao encontrado no banco tente adicionar como amigo primeiro para ele constar na lista ", idUsuario,
                bot)
            return True
        elif nomeMaker is None:
            funcoesBot.enviarMensagem(
                "maker nao encontrado no banco tente adicionar como amigo primeiro para ele constar na lista ", idUsuario,
                bot)
            return True
        else:
            retorno = usuarioTS.addMaker(nomeMain, nomeMaker, con)
            if retorno:
                funcoesBot.enviarMensagem(nomeMaker + " maker adicionado ao main: " + nomeMain, idUsuario, bot)
            else:
                funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botaddMakerUserTS "+e.__str__())
        return None


def botrmMakerUserTS(mensagemRecebida, con, idUsuario, bot):
    try:
        mensagemRecebida = mensagemRecebida.replace("!rmmaker ", "")
        nomeMain, nomeMaker = funcoesBot.pegarNomeMainEMaker(mensagemRecebida, con)
        if nomeMain is None:
            funcoesBot.enviarMensagem(
                "main nao encontrado no banco tente adicionar como amigo primeiro para ele constar na lista ", idUsuario,
                bot)
            return True
        elif nomeMaker is None:
            funcoesBot.enviarMensagem(
                "maker nao encontrado no banco tente adicionar como amigo primeiro para ele constar na lista ", idUsuario,
                bot)
            return True
        else:
            retorno = usuarioTS.rmMaker(nomeMain, nomeMaker, con)
            if retorno:
                funcoesBot.enviarMensagem(nomeMaker + " maker removido da lista do main: " + nomeMain, idUsuario, bot)
            else:
                funcoesBot.enviarMensagem(retorno, idUsuario, bot)
    except Exception as e:
        print("botrmMakerUserTS "+e.__str__())
        return None
