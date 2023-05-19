from spade import agent

from Behaviours.TorreDeControlo.enderecaPista import EnderecaPistaBehaviour
from Behaviours.TorreDeControlo.listenTorreControlo import ListenTorreControloBehaviour
from Behaviours.TorreDeControlo.enviaInfoDashboard import EnviaInfoDashboardBehaviour


class TorreDeControloAgent(agent.Agent):
    
    pistas_disp = 2
    gares_disp = 10 # depois criar um behaviour para ir buscar este valor ao gestor de gares
    lista_espera = []
    limite_espera = 10
    lista_aterrar = []
    lista_descolar = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        b1 = EnderecaPistaBehaviour(period=3)
        b2 = ListenTorreControloBehaviour()
        b3 = EnviaInfoDashboardBehaviour(period=5)
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        self.add_behaviour(b3)
