from spade import agent

class TorreDeControloAgent(agent.Agent):
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    