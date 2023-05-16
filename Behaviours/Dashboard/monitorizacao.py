from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.infoDashboard import InfoDashboard
from Templates.Aviao import Aviao


class MonitorizacaoBehaviour(CyclicBehaviour):

    async def run(self):

        msg = await self.receive(timeout=10) # wait for a message

        if msg.get_metadata('performative') == 'infoData':
            data : InfoDashboard
            data = jsonpickle.decode(msg.body)
            num_gares = data.get_num_gares_disp()
            num_pistas = data.get_num_pistas_disp()
            lista_espera = data.get_lista_espera()

            lista_espera_aterrar = list(filter(lambda x: x[1] == 'aterrar', lista_espera))
            lista_espera_descolar = list(filter(lambda x: x[1] == 'descolar', lista_espera))

            print("------------------- Info Dashboard -------------------")
            print(f"Numero de pistas disponiveis: {num_pistas}")
            print(f"Numero de gares disponiveis: {num_gares}")
            print(f"Lista de espera de aviões para aterrar:" )
            print(f"Lista de espera de aviões para aterrar: {lista_espera_aterrar}")
            print(f"Lista de espera de aviões para descolar: {lista_espera_descolar}")
            print("------------------------------------------------------")


