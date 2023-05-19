
class TorreDeControlo:
    pistas_disp = 2
    lista_espera = []
    limite_espera = 10
    gares_disp = 10 # depois criar um behaviour para ir buscar este valor ao gestor de gares
    lista_aterrar = []
    lista_descolar = []

    def __init__(self, x, y, pistas):
        self.x = x
        self.y = y
        self.pistas = pistas

    def add_pista(self, pista):
        self.pistas.append(pista)

    def pistas_disponiveis(self):
        return [x for x in self.pistas if x.is_available()]

    def dist(self, obj):
        return abs(self.x - obj.x) + abs(self.y - obj.y)
    
    def getBestPista(self, gares, aviao):
        '''
            Se retornar -1 é porque não há gares disponíveis
        '''
        pistas = self.pistas_disponiveis()
        if len(pistas) == 0:
            return -1

        shortestDists = []
        
        for pista in pistas:
            dists = []
            
            # Get closest gare
            for gare in gares:
                if gare.is_available() and gare.type == aviao.tipo:
                    dists.append(gare.dist(pista))
                else:
                    dists.append(float('inf'))

            if min(list) == float('inf'):
                shortestDists.append((-1,-1))
            else:
                min_dist = min(dists)
                shortestDists.append((gares.get(dists.index(min_dist)), min_dist))

        best_gare = sorted(shortestDists, lambda x: x[1])[0]
        best_pista = shortestDists.index(best_gare)

        if best_gare != -1 and best_pista != -1:
            #Reserva gare
            self.pistas[best_pista].land_plane(aviao)

        
        return best_pista, best_gare[0]

    def landing_completed(self, plane):
        for pista in self.pistas:
            if pista.landing_plane == plane:
                pista.landing_plane = None

