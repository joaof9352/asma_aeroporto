from spade import agent
import queue


class TorreDeControloAgent(agent.Agent):
    
    pistas_disp = 2
    espera_aterrar = []
    limite_espera = 10

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    