from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle


class ListenGestGaresBehaviour(CyclicBehaviour):

    async def run(self):

        msg = await self.receive()  # wait for a message

        if msg.get_metadata('performative') == 'requestNumGares':
            msgParaTorreControlo = Message(to=self.agent.get('Torre de Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyNumGares")
            msgParaTorreControlo.body = self.agent.get('gares_disp')

            await self.send(msgParaTorreControlo)

