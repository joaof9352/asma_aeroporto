from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

class GetNumGaresBehaviour(OneShotBehaviour):

    async def run(self):
        msg = Message(to=self.agent.get('Gestor De Gares'))  # Instantiate the message
        msg.set_metadata("performative", "getNumGares")
        await self.send(msg)

        msg = await self.receive(timeout=60) # wait for a message

        while msg.get_metadata("performative") != 'numGares':
            msg = await self.receive(timeout=60)
        
        if msg.get_metadata("performative") == 'numGares':
            numGaresComercial, numGaresMercadorias = int(msg.body.split(",")[0]), int(msg.body.split(",")[1])
            torreDeControlo = self.agent.get('TorreDeControlo')
            torreDeControlo.gares_disp_comercial = numGaresComercial
            torreDeControlo.gares_disp_mercadorias = numGaresMercadorias
            torreDeControlo.limite_espera = numGaresComercial + numGaresMercadorias
            self.agent.set('TorreDeControlo', torreDeControlo)


