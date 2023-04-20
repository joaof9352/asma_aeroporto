from spade import agent

class DashboardAgent(agent.Agent):
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    