from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.templateAviao import TemplateAviao

class VontadeAterrarBehaviour(OneShotBehaviour):
    
    async def run(self):
        print(f"Avião {self.jid} quer aterrar...")

        msg = Message(to=self.agent.get('Torre de Controlo'))  # Instantiate the message
        msg.set_metadata("performative", "requestLanding")
        template = TemplateAviao(self.jid, self.agent.get('Companhia'), self.agent.get('Tipo'), self.agent.get('Origem'), self.agent.get('Destino'))
        msg.body = jsonpickle.encode(template)
        await self.send(msg)



