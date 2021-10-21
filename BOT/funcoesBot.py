from __future__ import absolute_import
import time
import ts3
import BOT.comandosBot as comandosBot
from BD.Character import Character
from BOT.funcoesGerais import diferencaTempo
from Tibia import Character as charTibia

def botsSecundarios(settings, nome):
    try:
        conexao = ts3.query.TS3Connection(settings["host"], settings["port"])
        conexao.login(client_login_name=settings["username"], client_login_password=settings["password"])
        conexao.use(sid=settings["serverID"])
        conexao.clientupdate(client_nickname=nome.replace("[cspacer]", ""))
        conexao.servernotifyregister(event="textserver")
        conexao.servernotifyregister(event="textprivate")
        conexao.servernotifyregister(event="server")
        return conexao
    except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, Exception) as e:
        print("Bot Secundario"+e.__str__())
        pass



def notificaMorte(character,mensagem,bot,BDcon):
    try:
        if(character[8]==0):
            morreuPara="Mob"
        else:
            morreuPara="Player"

        if(character[7]!="0"):
            if(diferencaTempo(character)<10):
                if(character[9]==0):
                    pokeTodosClientes(mensagem+" "+character[1]+" Morreu Para: "+morreuPara+" as "+character[7],bot)
                    Character.updateNotificacaoMorte(character[0],BDcon)
                else:
                    Character.updateNotificacaoMorte(character[0], BDcon)
        else:
            Character.updateNotificacaoMorte(character[0], BDcon)
    except:
        pass


def pegaClid(nome, bot):
    try:
        return bot.clientfind(pattern=nome)[0]
    except:
        return None


def notificaMorteGuilda(character,mensagem,bot,BDcon):
    try:
        if(character[8]==0):
            morreuPara="Mob"
        else:
            deathPlayer=charTibia.getPlayer(character[1])
            morreuPara = "Player: "
            for players in deathPlayer.deaths[0]["killers"]:
                if players["player"]:
                    morreuPara=morreuPara+players["name"]+" , "


        if(character[7]!="0"):
            if(diferencaTempo(character)<10):
                if(character[9]==0):
                    pokeTodosClientes(mensagem+" "+character[1]+" Morreu Para: "+morreuPara+" as "+character[7],bot)
                    Character.updateNotificacaoMorte(character[0],BDcon)
                else:
                    Character.updateNotificacaoMorte(character[0], BDcon)
        else:
            Character.updateNotificacaoMorte(character[0], BDcon)
    except:
        pass


def pegaClid(nome, bot):
    try:
        return bot.clientfind(pattern=nome)[0]
    except:
        return None

def pegaBDId(uidUsuario, bot):
    try:
        return bot.clientdbfind(pattern=uidUsuario, uid=True)[0]["cldbid"].strip()
    except:
        return None

def pegarNomeMainEMaker(mensagemRecebida,con):
    mainName=""
    makerName=""
    for player in Character.selectAll(con):
        name=player[1].lower()
        name=name+" "
        if(name in mensagemRecebida.lower()):
            mainName=player[1]
            break

    if(mainName==""):
        return None,None

    mensagemRecebida = mensagemRecebida.lower().replace(mainName.lower(),"")
    mensagemRecebida=mensagemRecebida+" "
    for player in Character.selectAll(con):
        name = player[1].lower()
        name = name+" "
        if (name in mensagemRecebida.lower()):
            makerName = player[1]
            break

    if(makerName==""):
        return mainName,None
    else:
        return mainName,makerName



def pegarNomeEUsuario(mensagemRecebida,bot):
    global clienteTS
    global nomeMain
    global usuarioUID
    global nomeTS
    try:
        for cliente in pegarListaClientes(bot):
            if int(cliente["client_type"]) != 1:
                nomeCliente=cliente["client_nickname"].lower()
                nomeCliente=nomeCliente+" "
                if(nomeCliente in mensagemRecebida.lower()):
                     clienteTS=cliente
                     break
        nomeTS = clienteTS["client_nickname"]
        mensagemRecebida=mensagemRecebida.lower()
        mensagemRecebida=mensagemRecebida.replace(clienteTS["client_nickname"].lower(),"",1)
        nomeMain=mensagemRecebida.rstrip().lstrip()
        usuarioUID=pegaUidUsuario(clienteTS["client_database_id"], bot)
        return nomeMain,nomeTS,usuarioUID
    except:
        return None,None,None




def pegaUidUsuario(usuario,bot):
    try:
        return bot.clientdbinfo(cldbid=usuario)[0]["client_unique_identifier"]
    except:
        return None

def pegarListaClientes(bot):
    try:
        listaSemAdm = []
        lista = bot.clientlist()
        for cliente in lista:
            if (cliente["client_type"] == "0"):
                listaSemAdm.append(cliente)
        return listaSemAdm

    except:
        return None

def pegarIdChannel(bot, channel):
        try:
            return bot.channelfind(pattern=channel)[0]["cid"].strip()
        except:
            return None

def pokeClienteNome(msg, nome, bot):
    try:
        cliente = pegaClid(nome, bot)
        pokeCliente(msg, cliente["clid"], bot)
        return True
    except:
        return None


def pokeCliente(msg, clid, bot):
    try:
        bot.clientpoke(msg=msg, clid=clid)
        return True

    except:
        return None


def pokeTodosClientes(msg, bot):
    try:
        enviouTudo=False
        for cliente in pegarListaClientes(bot):
            msgPartida=""
            if(len(msg)>100):
                for caracter in msg:
                    enviouTudo = False
                    msgPartida+=caracter
                    if(len(msgPartida)==100):
                        pokeCliente(msgPartida, cliente["clid"], bot)
                        msgPartida=""
                        enviouTudo=True
                if(not enviouTudo):
                    pokeCliente(msgPartida, cliente["clid"], bot)
            else:
                pokeCliente(msg, cliente["clid"], bot)
        return True
    except:
        return None


def enviarMensagem(msg, usuario, bot):
    try:
        bot.sendtextmessage(targetmode=1, target=usuario, msg=msg)
        return True
    except:
        return None


def pegarPermissoesCliente(idcliente, bot):
    try:
        return bot.clientinfo(clid=idcliente)[0]["client_servergroups"]
    except:
        return None




def canalExiste(nomeCanal,bot):
        try:
            correto = 0
            channnel = bot.channellist(topic=True)
            for canal in channnel:

                if nomeCanal.lower().encode("utf-8") in canal['channel_name'].lower().encode("utf-8"):
                    return True

            if correto == 1:
                return True
            else:
                return False
        except:
            return None


def trataCanaisComEspaco(stringCanais,bot):
    channnel = bot.channellist(topic=True)
    canalOrigem=""
    parouOrigem=False
    canalDestino=""
    parouDestino = False
    for palavra in stringCanais.split(" "):
        canalOrigem+=palavra
        for canal in channnel:
            canalOrigem=canalOrigem.rstrip().lstrip()
            if canal['channel_name'].encode("utf-8").lower() == canalOrigem.encode("utf-8").lower():
                canalOrigem = canal['channel_name']
                parouOrigem=True
                break
        if(parouOrigem):
            break
        canalOrigem+=" "

    stringCanais=stringCanais.lower().replace(canalOrigem.lower(),"",1).rstrip().lstrip()
    for palavra in stringCanais.split(" "):
        canalDestino+=palavra
        for canal in channnel:
            canalDestino = canalDestino.rstrip().lstrip()
            if canal['channel_name'].lower().encode("utf-8") == canalDestino.lower().encode("utf-8"):
                canalDestino = canal['channel_name']
                parouDestino=True

                break
        if(parouDestino):
            break
        canalDestino+=" "


    if(canalExiste(canalOrigem,bot)):
         if(canalExiste(canalDestino,bot)):
              return canalOrigem, canalDestino
         else:
              return canalOrigem,None
    else:
           if (canalExiste(canalDestino,bot)):
               return None, canalDestino
           else:
                return None,None

def botAfk(settings):
        tsconn = botsSecundarios(settings,settings["canalAfk"])
        while True:
            time.sleep(60)
            try:
                tsconn.send_keepalive()
                for cliente in tsconn.clientlist():
                    if int(cliente["client_type"]) != 1:
                        if int(pegarIdChannel(tsconn, settings["canalAfk"])) != int(cliente["cid"]):
                            if (tsconn.servergroupsbyclientid(cldbid=cliente['client_database_id'])[0]['name'] != 'Guest'):
                                if int(tsconn.clientinfo(clid=cliente["clid"])[0][
                                           'client_idle_time']) >= int(settings["tempoAFK"]) * 60 * 1000:
                                    tsconn.clientmove(cid=pegarIdChannel(tsconn, settings["canalAfk"]), clid=cliente["clid"])
            except Exception as e:
                print("Class funcoesBots.BotAFK: "+e.__str__())
                pass

#<--------------Interacoes com clientes-------------->

def enviarMensagemBoasVindas(event, bot):
    try:
        if "reasonid" in event[0]:
            if event[0]["client_unique_identifier"].strip() != "serveradmin" and event[0]['reasonid'] == '0':
                idUsuario = event[0]["clid"].strip()  # pega o id de chat do usuario
                nomeUsuario = event[0]["client_nickname"].strip()  # pega o nome do usuario
                enviarMensagem("\nBem vindo " + nomeUsuario + "\nPara ver comandos digite !help", idUsuario, bot)

    except:
        return None


def recebeComandos(event, bot, settings,con):
    try:
        if "msg" in event[0]:
            if "invokeruid" in event[0]:
                if event[0]["invokeruid"].strip() != "serveradmin":
                    mensagemRecebida = event[0]["msg"].lower()
                    nomeUsuario = event[0]["invokername"]
                    usuarioID = event[0]["invokerid"]
                    usuarioUID = event[0]["invokeruid"]
                    listaPermissoesEvocador=pegarPermissoesCliente(usuarioID, bot)
                    for itens in listaPermissoesEvocador.split(","):
                    #<---- COMANDOS TODOS USUARIOS REGISTRADOS ---->
                        if (int(itens) == settings["grupoEditor"] or int(itens) == settings["grupoServerAdmin"] or int(itens) == settings["grupoAdmin"] or int(itens) == settings["grupoMovedor"] or int(itens) == settings["grupoUsuario"]):
                            if ("!bot" in mensagemRecebida):
                                comandosBot.botBoasVindas(nomeUsuario, usuarioID, bot)
                                return True
                            elif ("!help" in mensagemRecebida):
                                comandosBot.botHelp(usuarioID, bot, settings)
                                return True
                            elif("!shared " in mensagemRecebida):
                                comandosBot.botShared(mensagemRecebida,nomeUsuario,usuarioID,bot)
                                return True
                    # <---- FIM COMANDOS TODOS USUARIOS REGISTRADOS ---->

                    # <---- COMANDOS MOVEDOR ACIMA---->
                        if (int(itens) == settings["grupoEditor"] or int(itens) == settings["grupoServerAdmin"] or int(itens) == settings["grupoAdmin"] or int(itens) == settings["grupoMovedor"]):
                            if ("!mp " in mensagemRecebida):
                                comandosBot.botMassPoke(mensagemRecebida,settings)
                                return True
                            elif("!mvch " in mensagemRecebida):
                                comandosBot.botMvCh(mensagemRecebida, usuarioID,bot)
                                return True


                    # <---- FIM COMANDOS MOVEDOR ACIMA---->

                    # <---- COMANDOS ADMIN ACIMA---->
                        if (int(itens) == settings["grupoEditor"] or int(itens) == settings["grupoServerAdmin"] or int(itens) == settings["grupoAdmin"]):
                            if("!adduser " in mensagemRecebida):
                                comandosBot.botaddUserTS(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!addmaker " in mensagemRecebida):
                                comandosBot.botaddMakerUserTS(mensagemRecebida, con, usuarioID, bot)
                                return True

                            elif ("!ltem" in mensagemRecebida):
                                comandosBot.botLtEm(con, usuarioID, bot)
                                return True

                            elif("ltfd"  in mensagemRecebida):
                                comandosBot.botLtfd(con, usuarioID, bot)
                                return True
                    # <---- FIM COMANDOS ADMIN ACIMA---->


                    # <---- COMANDOS SERVER ADMIN ACIMA---->
                        if (int(itens) == settings["grupoEditor"] or int(itens) == settings["grupoServerAdmin"]):
                            if ("!addfd " in mensagemRecebida):
                                comandosBot.botAddFd(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!addem " in mensagemRecebida):
                                comandosBot.botAddEm(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!rmfd " in mensagemRecebida):
                                comandosBot.botRmFd(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!rmem " in mensagemRecebida):
                                comandosBot.botRmEm(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif("!addfdgui " in mensagemRecebida):
                                comandosBot.botAddFdgui(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif("!rmfdgui " in mensagemRecebida):
                                comandosBot.botRmFdgui(mensagemRecebida,con,usuarioID,bot)
                                return True
                            elif ("!addemgui " in mensagemRecebida):
                                comandosBot.botAddEmgui(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!rmemgui " in mensagemRecebida):
                                comandosBot.botRmEmgui(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!rmuser " in mensagemRecebida):
                                comandosBot.botrmUserTS(mensagemRecebida, con, usuarioID, bot)
                                return True
                            elif ("!rmmaker " in mensagemRecebida):
                                comandosBot.botrmMakerUserTS(mensagemRecebida, con, usuarioID, bot)
                                return True


                    # <---- FIM COMANDOS SERVER ADMIN ACIMA---->

                    # <---- COMANDOS GRUPO EDITOR---->
                     #   if (int(itens) == settings["grupoEditor"]):
                      #       print("teste")
                    # <---- FIM COMANDOS GRUPO EDITOR--->
                    enviarMensagem("Voce nao tem permissoes para usar esse comando", usuarioID, bot)




    except Exception as e:
        print("Comandos Bot: " + e.__str__())

        return None
