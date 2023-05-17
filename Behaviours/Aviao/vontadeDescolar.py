from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.templateAviao import TemplateAviao
from Templates.Aviao import Aviao

class VontadeDescolarBehaviour(OneShotBehaviour):
    
    async def run(self):
        print(f"Avião {self.agent.jid} quer descolar...")

        msg = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
        msg.set_metadata("performative", "requestTakeOff")
        aviao : Aviao
        aviao = self.agent.get('Aviao')
        msg.body = jsonpickle.encode(aviao)
        await self.send(msg)
        



