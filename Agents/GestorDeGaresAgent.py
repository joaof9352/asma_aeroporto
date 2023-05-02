from spade import agent

class GestorDeGaresAgent(agent.Agent):
    

    gares_disp = 10


    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    