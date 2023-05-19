from Templates.Gare import Gare

class GestorDeGares:
    gares_disp = 10
    avioes_espera = []

    def __init__(self, x, y, gares):
        self.x = x
        self.y = y
        self.listaGares: list(Gare) = gares

    def bestGare(self, obj):
        dists = []
        for gare in self.listaGares:
            if gare.is_available():
                dists.append(gare.dist(obj))
            else:
                dists.append(float('inf'))

        if min(list) == float('inf'):
            return -1

        return self.listaGares.get(dists.index(min(dists))), min(dists) 
    
    def add_gare(self, gare):
        self.listaGares.append(gare)

    def reserve(self, gare, aviao):
        for g in self.gares:
            if g.x == gare.x and g.y == gare.y:
                g.park_aviao(aviao)
    

