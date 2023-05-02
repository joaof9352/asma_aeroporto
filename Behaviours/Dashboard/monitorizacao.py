from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.templateMonitorizacao import TemplateMonitorizacao

class MonitorizacaoBehaviour(PeriodicBehaviour):

    async def run(self):
        msg = Message(to=self.agent.get('Torre de Controlo'))  # Instantiate the message
        msg.set_metadata("performative", "requestData")
        await self.send(msg)

        msg = await self.receive(timeout=10) # wait for a message

        if msg.get_metadata('performative') == 'replyData':
            data = TemplateMonitorizacao(self.agent.get('Torre de Controlo'), msg.body)