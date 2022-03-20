import calendar
from datetime import timedelta
from enum import Enum


class diasDaSemana(Enum):
    Segunda = 0
    Terca = 1
    Quarta = 2
    Quinta = 3
    Sexta = 4
    Sabado = 5
    Domingo = 6


class agenda:
    def __init__(self, now):
        self.now = now
        self.mes = []

    def getAgenda(self):
        self.completaFinal()
        return self.mes

    def ultimoDiaDoMes(self):
        return self.now.replace(day=calendar.monthrange(self.now.year, self.now.month)[1]).date()

    def completaFinal(self):
        ultimodia = self.mes[len(self.mes) - 1][1].day
        for i in range(self.ultimoDiaDoMes().day - ultimodia):
            diavazio = []
            diaAnterior = self.mes[len(self.mes) - 1][1] + timedelta(days=1)
            diavazio.append(diasDaSemana(diaAnterior.weekday()))
            diavazio.append(diaAnterior)
            diavazio.append("<->")
            self.mes.append(diavazio)

    def agendar(self, data, evento):
        dia = []
        igual = False
        if (len(self.mes) == 0):
            dia.append(diasDaSemana(data.weekday()))
            dia.append(data)
            dia.append(evento)
        else:
            ultimoDia = self.mes[len(self.mes) - 1][1].day
            while (ultimoDia < data.day - 1):
                if (self.mes[len(self.mes) - 1][1].day < data.day - 1):
                    diavazio = []
                    diaAnterior = self.mes[len(self.mes) - 1][1] + timedelta(days=1)
                    diavazio.append(diasDaSemana(diaAnterior.weekday()))
                    diavazio.append(diaAnterior)
                    diavazio.append("<->")
                    self.mes.append(diavazio)
                    ultimoDia = self.mes[len(self.mes) - 1][1].day

            for diaDoMes in self.mes:
                if (diaDoMes[1].day == data.day):
                    igual = True
                    self.index = self.mes.index(diaDoMes)
                    dia.append(diasDaSemana(data.weekday()))
                    dia.append(data)
                    dia.append(diaDoMes[2] + "\n" + evento)

        if (not igual and len(self.mes) > 0):
            dia.append(diasDaSemana(data.weekday()))
            dia.append(data)
            dia.append(evento)

        if (igual):
            self.mes[self.index] = dia
        else:
            self.mes.append(dia)
