from BOT import funcoesBot
import json
from BD.BD import BD
from BOT.AtualizaGuildas import AtualizaGuildas
from Auxiliares import tibiaRashid
from Auxiliares import tibiaBossesDreamCourts as DC
from Auxiliares import canalInimigoseAmigos
from Auxiliares import tibiaBossesFromGuildaStats
from Auxiliares import tempoAFK
from BOT import CanalEventos
from BOT import AtualizaUsuariosTS
from ThreadControle import Semaforo

import threading


def lerSettings():
    with open("settings.json", encoding="utf-8") as f:
        settings = json.load(f)
    return settings

def IniciarAtualizaGuildas(con,semaforo):
    atuali=AtualizaGuildas(con,semaforo)
    threading.Thread(name="Atualiza", target=atuali.iniciar).start()

def iniciaBotAFK(settings,tempo,semaforo):
    print("Inicia AFK")
    threading.Thread(name="BotAFK", target=funcoesBot.botAfk, args=(settings,tempo,semaforo,)).start()


def iniciarBotBosses(settings,semaforo):
    print("Inicia Tibia Bosses")
    tibiaBosses = tibiaBossesFromGuildaStats.tibiaBosses(settings,semaforo)
    threading.Thread(name="BOTBosses", target=tibiaBosses.iniciarBotCanalBoss).start()


def iniciarRashid(settings,semaforo):
    print("Inicia Tibia Rashid")
    threading.Thread(name="BOTRashid", target=tibiaRashid.rashidCidade, args=(settings,semaforo,)).start()


def iniciarDreamCourts(settings,semaforo,listaBoss):
    print("Inicia Tibia DreamCorts")
    threading.Thread(name="DreamCorts", target=DC.dreamCourts, args=(settings,semaforo,listaBoss,)).start()


def iniciarEventos(settings,semaforo):
    print("Inicia Tibia Eventos")
    eventos=CanalEventos.canalEventos(settings,semaforo)
    threading.Thread(name="BOTEventos", target=eventos.iniciar).start()

def iniciarCanalInimigoAmigo(settings,semaforo):
    print("Inicia Tibia Canal Inimigos")
    threading.Thread(name="BOTImigigos", target=canalInimigoseAmigos.iniciar, args=(settings,semaforo,)).start()

def iniciarAtualizaPermissoesUserTS(settings,semaforo):
    print("Inicia Atualiza Permissoes")
    threading.Thread(name="BotAtualizaPermissoes", target=AtualizaUsuariosTS.atualizaUsuariosTsChamada,args=(settings,semaforo,)).start()

if __name__ == '__main__':
    settings=lerSettings()
    Bd = BD(settings,settings["userBDMAIN"])
    print("Bot iniciado conectado ao servidor " + settings["host"] + ":" + settings["port"])
    botPrincipal = funcoesBot.botsSecundarios(settings, "Bot-Ts3")
    semaforo= Semaforo.Semaforo()

    tempo=tempoAFK.tempoAFK(settings)

    iniciaBotAFK(settings,tempo,semaforo)
    iniciarBotBosses(settings,semaforo)
    iniciarRashid(settings,semaforo)
    listaBoss=DC.ListaDreamCourtsCircular()
    iniciarDreamCourts(settings,semaforo,listaBoss)

    iniciarEventos(settings,semaforo)
    iniciarCanalInimigoAmigo(settings,semaforo)
    IniciarAtualizaGuildas(BD(settings,settings["userBDUPDATE"]),semaforo)
    iniciarAtualizaPermissoesUserTS(settings,semaforo)





    while (True):
            try:
                botPrincipal.send_keepalive()
                event = botPrincipal.wait_for_event(timeout=30)
                if "msg" in event[0]:
                    if "invokeruid" in event[0]:
                        if event[0]["invokeruid"].strip() != "serveradmin":
                            funcoesBot.recebeComandos(event,botPrincipal,settings,Bd,tempo,listaBoss)
                elif "reasonid" in event[0]:
                    if(event[0]['reasonid'] == '0'):
                        if event[0]["client_unique_identifier"].strip() != "serveradmin" :
                            funcoesBot.enviarMensagemBoasVindas(event, botPrincipal)

            except Exception as e:
                if(e.__str__()=="Could not receive data from the server within the timeout."):
                    pass
                else:
                    print("Principal: " + e.__str__())
                pass
            except KeyboardInterrupt:
                print("Finalizando KeyboardInterrupt")
                break





