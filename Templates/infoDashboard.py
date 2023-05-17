from Templates.Aviao import Aviao

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
    
    def print_lista_espera(self, lista_espera):
        str = "["
        i = 0
        for aviao in lista_espera:
            aviao : Aviao
            if i != len(lista_espera)-1: # se não for o ultimo elemento
                str += aviao.__str__() + ", "
            else:
                str += aviao.__str__()
            i += 1
        return str + "]"

    def __str__(self):
        lista_espera_aterrar = list(filter(lambda x: x[1] == 'aterrar', self.lista_espera))
        lista_espera_descolar = list(filter(lambda x: x[1] == 'descolar', self.lista_espera))
        print("\n\n\n\n------------------- Info Dashboard -------------------")
        print(f"Numero de pistas disponiveis: {self.num_pistas_disp}")
        print(f"Numero de gares disponiveis: {self.num_gares_disp}")
        print(f"Lista de espera de aviões para aterrar: {self.print_lista_espera(lista_espera_aterrar)}")
        print(f"Lista de espera de aviões para descolar: {self.print_lista_espera(lista_espera_descolar)}")
        print("------------------------------------------------------\n\n\n\n")