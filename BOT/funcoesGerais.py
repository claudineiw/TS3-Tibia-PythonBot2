from Auxiliares import data


def calculoShared(level, nomeUsuario):
    try:
        lvlMinimo = int(round(level / 1.5, 0))
        lvlMaximo = int(round(level * 1.5, 0))
        mensagem = nomeUsuario + ": voce pode sharear exp do level:" + str(lvlMinimo) + " ate o level:" + str(lvlMaximo)
        return mensagem
    except:
        return None


def diferencaTempo(character):
    return data.geHoraAtual(character[7])
