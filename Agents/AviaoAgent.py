from spade import agent

from Behaviours.Aviao.espConfirmacao import EspConfirmacaoBehaviour
from Behaviours.Aviao.vontadeAterrar import VontadeAterrarBehaviour
from Behaviours.Aviao.vontadeDescolar import VontadeDescolarBehaviour


class AviaoAgent(agent.Agent):
    
    #Escolher estas variáveis de acordo com uma lista predefinida de opções

    companhia = ""
    tipo = ""
    origem = ""
    destino = ""
    limite_timeout = 100
    tempo_aterragem = 20
    tempo_descolagem = 20

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        b1 = EspConfirmacaoBehaviour()
        b2 = VontadeAterrarBehaviour()
        b3 = VontadeDescolarBehaviour()
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        self.add_behaviour(b3)

    