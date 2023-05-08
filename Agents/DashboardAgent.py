from spade import agent

from Behaviours.Dashboard.monitorizacao import MonitorizacaoBehaviour


class DashboardAgent(agent.Agent):
    
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        b = MonitorizacaoBehaviour()
        self.add_behaviour(b)
    