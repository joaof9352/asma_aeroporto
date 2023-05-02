
class Monitorizacao():
    def __init__(self, pistas_disp, gares_disp, espera_aterrar, num_aterrar, num_descolar):
        self.pistas_disp = pistas_disp
        self.gares_disp = gares_disp
        self.espera_aterrar = espera_aterrar
        self.num_aterrar = num_aterrar
        self.num_descolar = num_descolar
    
    def getPistasDisp(self):
        return self.pistas_disp
    
    def getGaresDisp(self):
        return self.gares_disp
    
    def getEsperaAterrar(self):
        return self.espera_aterrar
    
    def getNumAterrar(self):
        return self.num_aterrar
    
    def getNumDescolar(self):
        return self.num_descolar
    
    def setPistasDisp(self, pistas_disp):
        self.pistas_disp = pistas_disp

    def setGaresDisp(self, gares_disp):
        self.gares_disp = gares_disp

    def setEsperaAterrar(self, espera_aterrar):
        self.espera_aterrar = espera_aterrar

    def setNumAterrar(self, num_aterrar):
        self.num_aterrar = num_aterrar

    def setNumDescolar(self, num_descolar):
        self.num_descolar = num_descolar