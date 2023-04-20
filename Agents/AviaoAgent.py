from spade import agent

class AviaoAgent(agent.Agent):
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    