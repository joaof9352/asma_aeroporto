from spade import agent

from Behaviours.GestorGares.listenGestGares import ListenGestGaresBehaviour
from Templates.GestorDeGares import GestorDeGares
from Templates.Gare import Gare

class GestorDeGaresAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        gares = [
            Gare(17, 5, 'COMERCIAL'),
            Gare(19, 5, 'MERCADORIAS'),
            Gare(21, 5, 'COMERCIAL'),
            Gare(8, 5, 'COMERCIAL'),
            Gare(9, 5, 'MERCADORIAS'),
            Gare(10, 5, 'COMERCIAL')
        ]
        gestor_de_gares = GestorDeGares(4, 4, gares)
        self.set('GestorDeGares', gestor_de_gares)

        b = ListenGestGaresBehaviour()
        self.add_behaviour(b)