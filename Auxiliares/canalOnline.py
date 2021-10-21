from BOT.funcoesBot import *
from BD.Character import Character
from BD.usuarioTS import usuarioTS

def onlineSr(player,con,tscon,listaClientesOnline):
    usuarios=usuarioTS.select(con)
    encontrado=False
    uid=""
    for usuario in usuarios:
        if(player[0]==usuario[2]):
            encontrado=True
            uid=usuario[4]
            dbIdUsuario = tscon.clientdbfind(pattern=usuario[4], uid=True)[0]['cldbid']
            for onlineTS in listaClientesOnline:
                if (onlineTS["client_database_id"] == dbIdUsuario):
                    return "ON"



    for usuario in usuarios:
       if(uid!=usuario[4]):
           if (player[0] == usuario[2]):
                encontrado = True
                dbIdUsuario = tscon.clientdbfind(pattern=usuario[4], uid=True)[0]['cldbid']
                for onlineTS in listaClientesOnline:
                    if (onlineTS["client_database_id"] == dbIdUsuario):
                        return "ON"

    if(encontrado==False):
        for usuario in usuarios:
            if (not usuario[3] is None):
                if(len(usuario[3]) > 0):
                    dbIdUsuario = tscon.clientdbfind(pattern=usuario[4], uid=True)[0]['cldbid']
                    for maker in usuario[3]:
                        if (player[0] == maker):
                            encontrado=True
                            for onlineTS in listaClientesOnline:
                                if(onlineTS["client_database_id"]==dbIdUsuario):
                                    return "ON"

    if(encontrado):
        return "OFF"
    else:
        return "SR"

def CanalOnline(tsconn, settings, BDcon):
    try:
        listaClientesOnline=tsconn.clientlist()
        tsconn.send_keepalive()
        descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn, settings["onlineTS"]))[0]["channel_description"]
        novaDescricao = "[table][tr][td]Nome[/td][td]Level[/td][td]TS[/td][/tr]"
        todosPlayersOnlineGuilda = Character.selectAllFromGuilOnline(BDcon,settings["nomeGuilda"])
        totalGuilda = Character.selectTotalPlayersGuild(BDcon,settings["nomeGuilda"])
        if not todosPlayersOnlineGuilda is None and not totalGuilda is None:
            contGuildOnline = 0
            if todosPlayersOnlineGuilda != False:
                for playerOnlineGuilda in todosPlayersOnlineGuilda:
                    contGuildOnline += 1
                    novaDescricao += "[tr][td]" + playerOnlineGuilda[1] + "[/td][td]" + str(playerOnlineGuilda[2]) + "[/td][td]"+onlineSr(playerOnlineGuilda,BDcon,tsconn,listaClientesOnline)+"[/td][/tr]"
                novaDescricao += "[/table]"
                if descricao != novaDescricao:
                    nomeAtual = (tsconn.channelinfo(cid=int(pegarIdChannel(tsconn, settings["onlineTS"])))[0]["channel_name"])
                    novoNome = settings["onlineTS"] + " (" + str(contGuildOnline) + "/" + str(totalGuilda[0][0]) + ")"
                    if nomeAtual != novoNome:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["onlineTS"]), channel_description=novaDescricao.strip(), channel_name=novoNome)
                    else:
                        tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["onlineTS"]),  channel_description=novaDescricao.strip())

    except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError):
        pass




