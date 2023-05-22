from Templates.Gare import Gare

class GestorDeGares:
    avioes_espera = []

    def __init__(self, x, y, gares):
        self.x = x
        self.y = y
        self.listaGares: list(Gare) = gares
        self.gares_disp_comercial = len(list(filter(lambda x: x.get_tipo() == "COMERCIAL",gares)))
        self.gares_disp_mercadorias = len(list(filter(lambda x: x.get_tipo() == "MERCADORIAS",gares)))


    def add_gare(self, gare):
        self.listaGares.append(gare)

    def reserve(self, gare, aviao):
        for g in self.listaGares:
            if g.x == gare.x and g.y == gare.y:
                g.park_aviao(aviao)

    def free_gare(self, aviao):
        for g in self.listaGares:
            if g.get_aviao() is not None:
                if g.aviao.get_jid() == aviao.get_jid():
                    g.free_gare()
    
    def get_gare_aviao(self, aviao):
        for g in self.listaGares:
            if g.get_aviao() is not None:
                if g.get_aviao().get_jid() == aviao.get_jid():
                    return g


