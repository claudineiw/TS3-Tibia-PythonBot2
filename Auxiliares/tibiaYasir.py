import requests
from BOT.funcoesBot import *
def yasirOnline(settings):
    params = {
        "api_key": "tta37se2v8pG",
        "format": "json"
    }
    while True:
        try:
            tsconn = botsSecundarios(settings,"BOTYasir")
            requests.post('https://www.parsehub.com/api/v2/projects/t16skBSvK_iT/run', params=params)
            r = requests.get('https://www.parsehub.com/api/v2/projects/t16skBSvK_iT/last_ready_run/data', params=params)
            texto = r.json()
            novaDescricao = "[table][tr][td][COLOR=blue]Mundo[/td][td][COLOR=blue]Cidade[/td][/tr]"

            for itens in texto["Onlines"]:
                novaDescricao += "[tr][td][COLOR=green]" + itens["Mundo"] + "[/td][td][COLOR=green]" + itens[
                    "Cidade"] + "[/td][/tr]"
            novaDescricao += "[/table]"
            novaDescricao += "[table][tr][td][/td][td][/td][/tr][tr][td][/td][td][/td][/tr][tr][td][COLOR=blue]Mundo[/td][td][COLOR=blue]Dias sem Yasir[/td][/tr]"
            for itens in texto["Offline"]:
                novaDescricao += "[tr][td][COLOR=red]" + itens["Mundo"] + "[/td][td][COLOR=red]" + itens[
                    "DiasSemYasir"] + "[/td][/tr]"

            novaDescricao += "[/table]"
            descricao = tsconn.channelinfo(cid=pegarIdChannel(tsconn,settings["canalYasir"]))[0][
                "channel_description"]
            if novaDescricao != descricao:
                tsconn.channeledit(cid=pegarIdChannel(tsconn, settings["canalYasir"]),
                                   channel_description=novaDescricao)
            tsconn.close()
            time.sleep(3600)

        except (ts3.query.TS3QueryError, ts3.query.TS3TimeoutError, ts3.query.TS3RecvError, IndexError, ValueError,
                KeyError, TypeError, AttributeError):
            pass