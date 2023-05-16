class InfoDashboard():

    def __init__(self, num_pistas_disp, num_gares_disp, lista_espera):
        self.num_pistas_disp = num_pistas_disp
        self.num_gares_disp = num_gares_disp
        self.lista_espera = lista_espera
    
    def get_num_pistas_disp(self):
        return self.num_pistas_disp
    
    def get_num_gares_disp(self):
        return self.num_gares_disp
    
    def get_lista_espera(self):
        return self.lista_espera
    
    def set_num_pistas_disp(self, num_pistas_disp):
        self.num_pistas_disp = num_pistas_disp

    def set_num_gares_disp(self, num_gares_disp):
        self.num_gares_disp = num_gares_disp

    def set_lista_espera(self, lista_espera):
        self.lista_espera = lista_espera

