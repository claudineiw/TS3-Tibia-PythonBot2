def listaHelp(clienteServerGroupsID, settings):
    try:

            if str(settings["grupoEditor"]) in  clienteServerGroupsID:
                return ("\n Voce pode usar:"
                        "\n !shared level. Verificar level minimo e maximo para compartilhamento de exp"
                        "\n !mp msg. Mandar um poke para todos os usuarios do TS3"
                        "\n !mv canal. Mover todos os usuarios do TS3 para um canal"
                        "\n !afk tempo. Altera o tempo de mover do AFK deve ser passado o tempo em minutos"
                        "\n !mvch origem destino. Mover usuarios de um canal para outro"
                        "\n !addfd Nome personagem. Adicionar personagem na lista amigos"
                        "\n !rmfd Nome personagem. Remover personagem na lista amigos"
                        "\n !addfdgui Nome da guilda. Adicionar guilda na lista amigos"
                        "\n !rmfdgui Nome guilda. Remover guilda na lista amigos"
                        "\n !addem Nome personagem. Adicionar personagem na lista inimigos"
                        "\n !rmem Nome personagem. Remover personagem na lista inimigos"
                        "\n !ltfd mostra lista de amigos"
                        "\n !ltem mostra lista de inimigos"),(
                        "\n !ltuser mostra lista de usuarios"
                        "\n !addemgui Nome da guilda. Adicionar guilda na lista inimigos"
                        "\n !rmemgui Nome guilda. Remover guilda na lista inimigos"
                        "\n !adduser <NomeUsuario> <Main> adicionar usuario ao banco de dados"
                        "\n !rmuser <Main> remover usuario ao banco de dados"
                        "\n !addmaker <NomeMain> <NomeMaker> adicionar maker ao main no banco de dados"
                        "\n !rmmmaker <NomeMain> <NomeMaker> remover maker do main no banco de dados"
                        "\n !boss <mensagem> Mass Poke para usuarios do grupoBoss"
                        "\n !sell <mensagem> Mass Poke para usuarios do grupoVendas"
                        )


            elif str(settings["grupoServerAdmin"]) in  clienteServerGroupsID:
                return ("\n Voce pode usar:"
                        "\n !shared level. Verificar level minimo e maximo para compartilhamento de exp"
                        "\n !mp msg. Mandar um poke para todos os usuarios do TS"
                        "\n !mvch origem destino. Mover usuarios de um canal para outro"
                        "\n !addfd Nome personagem. Adicionar personagem na lista amigos"
                        "\n !rmfd Nome personagem. Remover personagem na lista amigos"
                        "\n !addfdgui Nome da guilda. Adicionar guilda na lista amigos"
                        "\n !rmfdgui Nome guilda. Remover guilda na lista amigos"
                        "\n !addem Nome personagem. Adicionar personagem na lista inimigos"
                        "\n !rmem Nome personagem. Remover personagem na lista inimigos"
                        "\n !ltfd mostra lista de amigos"
                        "\n !ltem mostra lista de inimigos"),(
                        "\n !ltuser mostra lista de usuarios"
                        "\n !addemgui Nome da guilda. Adicionar guilda na lista inimigos"
                        "\n !rmemgui Nome guilda. Remover guilda na lista inimigos"
                        "\n !adduser <NomeUsuario> <Main> adicionar usuario ao banco de dados"
                        "\n !rmuser <Main> remover usuario ao banco de dados"
                        "\n !addmaker <NomeMain> <NomeMaker> adicionar maker ao main no banco de dados"
                        "\n !rmmmaker <NomeMain> <NomeMaker> remover maker do main no banco de dados"
                        "\n !boss <mensagem> Mass Poke para usuarios do grupoBoss"
                        "\n !sell <mensagem> Mass Poke para usuarios do grupoVendas"
                        )

            elif str(settings["grupoAdmin"])  in  clienteServerGroupsID:
                return ("\n Voce pode usar:"
                        "\n !shared level. Verificar level minimo e maximo para compartilhamento de exp"
                        "\n !mp msg. Mandar um poke para todos os usuarios do TS3"
                        "\n !mvch origem destino. Mover usuarios de um canal para outro"
                        "\n !addfd Nome personagem. Adicionar personagem na lista amigos"
                        "\n !addem Nome personagem. Adicionar personagem na lista inimigos"   
                        "\n !ltfd mostra lista de amigos"
                        "\n !ltem mostra lista de inimigos"
                        "\n !ltuser mostra lista de usuarios"
                         "\n !adduser <NomeUsuario> <Main> adicionar usuario ao banco de dados"
                        "\n !addmaker <NomeMain> <NomeMaker> adicionar maker ao main no banco de dados"
                        "\n !boss <mensagem> Mass Poke para usuarios do grupoBoss"
                        "\n !sell <mensagem> Mass Poke para usuarios do grupoVendas"
                        ),()

            elif str(settings["grupoMovedor"])  in  clienteServerGroupsID:
                return ("\n Voce pode usar:"
                        "\n !shared level. Verificar level minimo e maximo para compartilhamento de exp"
                        "\n !mp msg. Mandar um poke para todos os usuarios do TS3"
                        "\n !mvch origem destino. Mover usuarios de um canal para outro"
                        "\n !boss <mensagem> Mass Poke para usuarios do grupoBoss"
                        "\n !sell <mensagem> Mass Poke para usuarios do grupoVendas"
                        ),()

            elif str(settings["grupoUsuario"])   in  clienteServerGroupsID:
                return ("\n Voce pode usar:"
                        "\n !shared level. Verificar level minimo e maximo para compartilhamento de exp"
                        "\n !boss <mensagem> Mass Poke para usuarios do grupoBoss"
                        "\n !sell <mensagem> Mass Poke para usuarios do grupoVendas"
                        ),()
            else:
                return "Voce nao pode usar o bot"
    except Exception as e:
        print("Lista Help: "+e.__str__())
        return None
