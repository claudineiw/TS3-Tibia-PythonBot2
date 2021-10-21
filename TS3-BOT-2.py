from BOT import funcoesBot
import json
from BD.BD import BD
from BOT.AtualizaGuildas import AtualizaGuildas
from Auxiliares import tibiaBosses
from Auxiliares import tibiaRashid
from Auxiliares import tibiaYasir
from Auxiliares import canalInimigoseAmigos
from BOT import AtualizaUsuariosTS
import threading


def lerSettings():
    with open("settings.json", encoding="utf-8") as f:
        settings = json.load(f)
    return settings

def atualiza(con):
    atuali=AtualizaGuildas(con)
    threading.Thread(name="Atualiza", target=atuali.iniciar).start()

def iniciaBotAFK(settings):
    print("Inicia AFK")
    threading.Thread(name="BotAFK", target=funcoesBot.botAfk, args=(settings,)).start()


def iniciarBotBosses(settings):
    print("Inicia Tibia Bosses")
    threading.Thread(name="BOTBosses", target=tibiaBosses.tibiaBosses, args=(settings,)).start()


def iniciarRashid(settings):
    print("Inicia Tibia Rashid")
    threading.Thread(name="BOTRashid", target=tibiaRashid.rashidCidade, args=(settings,)).start()


def iniciaYasir(settings):
    print("Inicia Tibia Yasir")
    threading.Thread(name="BOTYasir", target=tibiaYasir.yasirOnline, args=(settings,)).start()

def canalInimigoAmigo(settings):
    print("Inicia Tibia Canal Inimigos")
    threading.Thread(name="BOTImigigos", target=canalInimigoseAmigos.iniciar, args=(settings,)).start()

def iniciarAtualizaPermissoesUserTS(settings):
    print("Inicia Atualiza Permissoes")
    threading.Thread(name="BotAtualizaPermissoes", target=AtualizaUsuariosTS.atualizaUsuariosTsChamada,args=(settings,)).start()

if __name__ == '__main__':
    settings=lerSettings()
    Bd = BD(settings,settings["userBDMAIN"])
    print("Bot iniciado conectado ao servidor " + settings["host"] + ":" + settings["port"])
    botPrincipal = funcoesBot.botsSecundarios(settings, "Bot-Ts3")
    iniciaBotAFK(settings)
  #  iniciarBotBosses(settings)
    iniciarRashid(settings)
    #iniciaYasir(settings) site fora do ar
    canalInimigoAmigo(settings)
    atualiza(BD(settings,settings["userBDUPDATE"]))
    iniciarAtualizaPermissoesUserTS(settings)
    while (True):
            try:
                botPrincipal.send_keepalive()
                event = botPrincipal.wait_for_event(timeout=30)
                funcoesBot.enviarMensagemBoasVindas(event, botPrincipal)
                funcoesBot.recebeComandos(event, botPrincipal,settings,Bd)
            except Exception as e:
                if(e.__str__()=="Could not receive data from the server within the timeout."):
                    pass
                else:
                    print("Principal: " + e.__str__())
                pass
            except KeyboardInterrupt:
                print("Finalizando KeyboardInterrupt")
                break





