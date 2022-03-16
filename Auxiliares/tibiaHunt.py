class tibiaHunt:
    def __init__(self,dados):
        self.dados=dados
        self.sessionDate=self.find_session_date()
        self.duracaoSession=self.find_session_duration()
        self.primeiroSplit()

    def primeiroSplit(self):
        self.dados=self.dados.replace(" (leader)","")
        self.remove_first_section()
        self.number_of_players = self.find_total_number_of_players()
        self.players_and_their_balance = self.find_players_and_balance()
        self.total_profit = self.find_total_profit()
        self.profit_per_person = self.total_profit / self.number_of_players
        self.who_to_pay_and_how_much=self.final_split()

    def find_session_date(self):
        return self.dados[19:29]


    def find_session_duration(self):
        index = self.dados.find("session: ")
        return self.dados[index + 9:index + 15]


    def remove_first_section(self):
            index = self.dados.find("balance: ")
            substring1 = self.dados[index + 9:]
            index2 = substring1.find("\n")
            substring2 = substring1[0:index2]
            self.dados = substring1[len(substring2) + 1:]

    def find_total_number_of_players(self):
        return self.dados.count("balance")


    def find_players_and_balance(self):
        players_and_balance = []
        player_names_list = []
        for x in range(self.number_of_players):
            index_loot = self.dados.find("loot:")
            name_of_player = self.dados[0:index_loot]
            name_of_player = name_of_player.strip()
            index_balance = self.dados.find("balance: ")
            index_damage = self.dados.find("damage: ")
            balance_of_player = self.dados[index_balance + 9:index_damage]
            balance_of_player = balance_of_player.strip()
            players_and_balance.append({'name': name_of_player,'balance': balance_of_player.replace(",",""),})
            player_names_list.append(name_of_player)
            index_healing = self.dados.find("healing: ")
            self.dados = self.dados[index_healing + 9:]
            index_space = self.dados.find("\n")
            self.dados = self.dados[index_space + 1:]
        return players_and_balance


    def find_total_profit(self):
        total_balance = 0
        for x in range(len(self.players_and_their_balance)):
            total_balance =  total_balance + int(self.players_and_their_balance[x]["balance"])
        return total_balance


    def final_split(self):
      players_and_outstanding_payment = []
      for i in range(self.number_of_players):
        name = self.players_and_their_balance[i]["name"]
        oustanding_payment = float(self.profit_per_person) - float(self.players_and_their_balance[i]["balance"])
        players_and_outstanding_payment.append({'name': name,'balance': oustanding_payment,})

      who_to_pay_and_how_much = []

      for i in range(self.number_of_players):
        if (players_and_outstanding_payment[i]["balance"] < 0):
          while (abs(players_and_outstanding_payment[i]["balance"]) > 5):
            for j in range(self.number_of_players):
              if (players_and_outstanding_payment[j]["balance"] > 0):
                if (players_and_outstanding_payment[j]["balance"] > abs(players_and_outstanding_payment[i]["balance"])):
                   players_and_outstanding_payment[j]["balance"] = players_and_outstanding_payment[j]["balance"] + players_and_outstanding_payment[i]["balance"]
                   who_to_pay_and_how_much.append({'name': players_and_outstanding_payment[i]["name"],'amount': abs(players_and_outstanding_payment[i]["balance"]),'to_who': players_and_outstanding_payment[j]["name"],})
                   players_and_outstanding_payment[i]["balance"] = 0
                else:
                  players_and_outstanding_payment[i]["balance"] = players_and_outstanding_payment[i]["balance"] +  players_and_outstanding_payment[j]["balance"]
                  players_and_outstanding_payment[j]["balance"] = round(players_and_outstanding_payment[j]["balance"])
                  who_to_pay_and_how_much.append({'name': players_and_outstanding_payment[i]["name"],'amount': abs(players_and_outstanding_payment[j]["balance"]),'to_who': players_and_outstanding_payment[j]["name"],})
                  players_and_outstanding_payment[j]["balance"] = 0
      return who_to_pay_and_how_much



    def getResult(self):
      transfer_array = []
      for i in range(len(self.who_to_pay_and_how_much)):
          amount = self.who_to_pay_and_how_much[i]["amount"]
          gp_amount = round(amount)
          payer_name = self.who_to_pay_and_how_much[i]["name"]
          payee_name = self.who_to_pay_and_how_much[i]["to_who"]
          if (amount != 0):
              if (amount > 1000):
                amount = round(amount / 1000)
                transfer_message = '{} tem que pagar {}k para {} (Bank: transfer {} to {})'.format(payer_name,amount,payee_name,gp_amount,payee_name)
                transfer_array.append(transfer_message)
              else:
                transfer_message ='{} tem que pagar {}k para {} (Bank: transfer {} to {})'.format(payer_name,gp_amount,payee_name,gp_amount,payee_name)
                transfer_array.append(transfer_message)

      return transfer_array
