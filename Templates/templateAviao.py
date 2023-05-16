class TemplateAviao():

    def __init__(self, aviao_jid, companhia, tipo, origem, destino):
        self.aviao_jid = aviao_jid
        self.companhia = companhia
        self.tipo = tipo
        self.origem = origem
        self.destino = destino
    
    def getAviaoJid(self):
        return self.aviao_jid
    
    def getCompanhia(self):
        return self.companhia
    
    def getTipo(self):
        return self.tipo
    
    def getOrigem(self):
        return self.origem
    
    def getDestino(self):
        return self.destino
    
    def setAviaoJid(self, aviao_jid):
        self.aviao_jid = aviao_jid

    def setCompanhia(self, companhia):
        self.companhia = companhia

    def setTipo(self, tipo):
        self.tipo = tipo

    def setOrigem(self, origem):
        self.origem = origem

    def setDestino(self, destino):
        self.destino = destino

    def __str__(self):
        return f"Aviao: {self.aviao_jid}, Companhia: {self.companhia}, Tipo: {self.tipo}, Origem: {self.origem}, Destino: {self.destino}"