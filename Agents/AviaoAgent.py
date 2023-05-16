from spade import agent

from Behaviours.Aviao.espConfirmacao import EspConfirmacaoBehaviour
from Behaviours.Aviao.vontadeAterrar import VontadeAterrarBehaviour
from Behaviours.Aviao.vontadeDescolar import VontadeDescolarBehaviour

from Templates.Aviao import Aviao

class AviaoAgent(agent.Agent):
    
    #Escolher estas variáveis de acordo com uma lista predefinida de opções
    

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        aviao = Aviao(self.jid)
        self.set('Aviao', aviao)

        b1 = EspConfirmacaoBehaviour()
        b2 = VontadeAterrarBehaviour()
        b3 = VontadeDescolarBehaviour()
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        self.add_behaviour(b3)

    