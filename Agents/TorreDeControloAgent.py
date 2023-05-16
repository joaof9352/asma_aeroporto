from spade import agent
import queue

from Behaviours.TorreDeControlo.enderecaPista import EnderecaPistaBehaviour
from Behaviours.TorreDeControlo.listenTorreControlo import ListenTorreControloBehaviour
from Behaviours.TorreDeControlo.enviaInfoDashboard import EnviaInfoDashboardBehaviour


class TorreDeControloAgent(agent.Agent):
    
    pistas_disp = 2
    lista_espera = []
    limite_espera = 10

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        b1 = EnderecaPistaBehaviour()
        b2 = ListenTorreControloBehaviour()
        b3 = EnviaInfoDashboardBehaviour(period=3)
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        self.add_behaviour(b3)
