from spade import agent

from Behaviours.Aviao.espConfirmacao import EspConfirmacaoBehaviour
from Behaviours.Aviao.vontadeAterrar import VontadeAterrarBehaviour
from Behaviours.Aviao.vontadeDescolar import VontadeDescolarBehaviour

from Templates.Aviao import Aviao

class AviaoAgent(agent.Agent):
    

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        aviao = Aviao(f"{self.jid}")
        self.set('Aviao', aviao)

        b1 = EspConfirmacaoBehaviour()
        b2 = VontadeAterrarBehaviour()
        b3 = VontadeDescolarBehaviour()
        self.add_behaviour(b1)
        self.add_behaviour(b2)
        #self.add_behaviour(b3)



"""
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour

class MyBehaviour(OneShotBehaviour):
    async def run(self):
        print("Executing MyBehaviour")
        # Call AnotherBehaviour after 5 seconds
        self.agent.call_later(5, self.agent.start_behaviour, AnotherBehaviour())

class AnotherBehaviour(CyclicBehaviour):
    async def run(self):
        print("Executing AnotherBehaviour")
        # Perform the desired actions of AnotherBehaviour

class MyAgent(Agent):
    async def setup(self):
        self.add_behaviour(MyBehaviour())

my_agent = MyAgent("agent@example.com", "password")
my_agent.start()
"""

    