import random

"""

"""

class Aviao():
    companhias = ["Emirates", "TAP", "Ryanair", "EasyJet", "Malta Airlines", "Turkish Airlines"]
    tipo = ["MERCADORIAS", "COMERCIAL"]
    locais = ["Lisboa", "Madrid", "Barcelona", "Paris", "Londres", "Berlim", "Istambul", "Atenas", "Amsterdão", "Viena", "Dublin", "Budapeste"]

    def __init__(self, jid, x, y):
        self.jid = jid
        self.companhia = random.choice(self.companhias)
        self.tipo = random.choice(self.tipo)
        self.origem = random.choice(self.locais)
        self.destino = "Porto"
        self.limite_timeout = random.randint(30,60)
        self.tempo_aterragem = 20
        self.tempo_descolagem = 20
        self.x = x
        self.y = y

    def get_jid(self):
        return self.jid

    def get_companhia(self):
        return self.companhia
    
    def get_tipo(self):
        return self.tipo
    
    def get_origem(self):
        return self.origem
    
    def get_destino(self):
        return self.destino
    
    def get_limite_timeout(self):
        return self.limite_timeout
    
    def get_tempo_aterragem(self):
        return self.tempo_aterragem
    
    def get_tempo_descolagem(self):
        return self.tempo_descolagem
    
    def set_jid(self, jid):
        self.jid = jid
    
    def set_companhia(self, companhia):
        self.companhia = companhia

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_origem(self, origem):
        self.origem = origem

    def set_destino(self, destino):
        self.destino = destino

    def set_limite_timeout(self, limite_timeout):
        self.limite_timeout = limite_timeout

    def set_tempo_aterragem(self, tempo_aterragem):
        self.tempo_aterragem = tempo_aterragem

    def set_tempo_descolagem(self, tempo_descolagem):
        self.tempo_descolagem = tempo_descolagem


    def __str__(self):
        return f"Aviao: {self.jid}, Companhia: {self.companhia}, Tipo: {self.tipo}, Origem: {self.origem}, Destino: {self.destino}, Limite Timeout: {self.limite_timeout}, Tempo Aterragem: {self.tempo_aterragem}, Tempo Descolagem: {self.tempo_descolagem}\n"

    