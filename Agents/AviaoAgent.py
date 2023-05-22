from spade import agent

from Behaviours.Aviao.espConfirmacao import EspConfirmacaoBehaviour
from Behaviours.Aviao.vontadeAterrar import VontadeAterrarBehaviour
from Behaviours.Aviao.vontadeDescolar import VontadeDescolarBehaviour

from Templates.Aviao import Aviao

class AviaoAgent(agent.Agent):
    

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        aviao = Aviao(f"{self.jid}", 300, 5)
        self.set('Aviao', aviao)
        self.set('quer_aterrar', False)

        b1 = EspConfirmacaoBehaviour()
        b2 = VontadeAterrarBehaviour()
        self.add_behaviour(b1)
        self.add_behaviour(b2)
    