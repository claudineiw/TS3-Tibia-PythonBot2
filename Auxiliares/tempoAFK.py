class tempoAFK:
    def __init__(self,settings):
        self.canalAFK=settings["canalAfk"]
        self.tempoAFK=settings["tempoAFK"]

    def setTempo(self,novoTempo):
        self.tempoAFK=novoTempo