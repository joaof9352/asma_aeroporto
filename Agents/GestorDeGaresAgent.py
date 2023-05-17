from spade import agent

from Behaviours.GestorGares.listenGestGares import ListenGestGaresBehaviour

class GestorDeGaresAgent(agent.Agent):
    

    gares_disp = 10
    avioes_espera = []

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        b = ListenGestGaresBehaviour()
        self.add_behaviour(b)
