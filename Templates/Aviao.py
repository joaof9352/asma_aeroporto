import random

"""

"""

class Aviao():

    companhias = ["Emirates", "TAP", "Ryanair", "EasyJet", "Malta Airlines", "Turkish Airlines"]
    tipo = ["Comercial", "Mercadorias"]
    locais = ["Lisboa", "Porto", "Madrid", "Barcelona", "Paris", "Londres", "Berlim", "Istambul", "Atenas", "Amsterdão", "Viena", "Dublin", "Budapeste"]

    def __init__(self, jid):
        jid = jid
        companhia = random.choice(self.companhia)
        tipo = random.choice(self.tipo)
        origem = random.choice(self.locais)
        destino = random.choice([x for x in self.locais if x != origem])
        limite_timeout = random.randint(30, 60)
        tempo_aterragem = 20
        tempo_descolagem = 20

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

    