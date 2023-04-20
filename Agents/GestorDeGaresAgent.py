from spade import agent

class GestorDeGaresAgent(agent.Agent):
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    