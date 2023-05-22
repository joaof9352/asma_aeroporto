
class TorreDeControlo:
    pistas_disp = 2
    lista_espera = []
    limite_espera = 10         # Isto agora está a ser alterado pelo behaviour GetNumGaresBehaviour
    gares_disp_mercadorias = 2 # Isto agora está a ser alterado pelo behaviour GetNumGaresBehaviour
    gares_disp_comercial = 4   # Isto agora está a ser alterado pelo behaviour GetNumGaresBehaviour
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
            return None, None

        shortestDists = []
        
        for pista in pistas:
            dists = []
            
            # Get closest gare
            for gare in gares:
                if gare.is_available() and gare.type == aviao.tipo:
                    dists.append(gare.dist(pista))
                else:
                    dists.append(float('inf'))

            if min(dists) == float('inf'):
                shortestDists.append((None,float('inf')))
            else:
                min_dist = min(dists)
                shortestDists.append((gares[dists.index(min_dist)], min_dist))

        best_gare = sorted(shortestDists, key=lambda x: x[1])[0]

        if best_gare[0] is None:
            return None, None
        
        best_pista = shortestDists.index(best_gare)
        return pistas[best_pista], best_gare[0]
    
    def get_best_pista_descolagem(self, gare):
        '''
            Retorna a pista mais perto de determinada gare. Se todas estiverem ocupadas retorna -1.
        '''

        shortestDists = []
        for pista in self.pistas:
            if pista.is_available():
                shortestDists.append(pista.dist(gare))
            else:
                shortestDists.append(float('inf'))

        if min(shortestDists) == float('inf'):
                return None
        else:
            min_dist = min(shortestDists)
            return self.pistas[shortestDists.index(min_dist)]


    def landing_completed(self, plane):
        for pista in self.pistas:
            #print(f'Assigned Plane: {pista.assigned_plane.get_jid()}')
            if not pista.is_available():
                if pista.assigned_plane.get_jid() == plane.get_jid():
                    pista.free_pista()