from Templates.Gare import Gare

class GestorDeGares:
    avioes_espera = []

    def __init__(self, x, y, gares):
        self.x = x
        self.y = y
        self.listaGares: list(Gare) = gares
        self.gares_disp = len(gares)
    
    def add_gare(self, gare):
        self.listaGares.append(gare)

    def reserve(self, gare, aviao):
        for g in self.listaGares:
            if g == gare:
                g.park_aviao(aviao)

    def free_gare(self, aviao):
        for g in self.gares:
            if g.aviao == aviao:
                g.free_gare()
    
    def get_gare_aviao(self, aviao):
        for g in self.listaGares:
            if g.aviao == aviao:
                return g


