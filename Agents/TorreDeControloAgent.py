from spade import agent

from Behaviours.TorreDeControlo.enderecaPista import EnderecaPistaBehaviour
from Behaviours.TorreDeControlo.listenTorreControlo import ListenTorreControloBehaviour
from Behaviours.TorreDeControlo.enviaInfoDashboard import EnviaInfoDashboardBehaviour
from Templates.TorreDeControlo import TorreDeControlo
from Templates.Pista import Pista


class TorreDeControloAgent(agent.Agent):
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        torre_de_controlo = TorreDeControlo(11, 5, [Pista(13, 5), Pista(14, 5), Pista(15, 5)])
        self.set('TorreDeControlo', torre_de_controlo)

        b1 = EnderecaPistaBehaviour(period=3)
        b2 = ListenTorreControloBehaviour()
        b3 = EnviaInfoDashboardBehaviour(period=5)
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        self.add_behaviour(b3)
