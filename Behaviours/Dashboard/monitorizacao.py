from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.infoDashboard import InfoDashboard
from Templates.Aviao import Aviao


class MonitorizacaoBehaviour(CyclicBehaviour):

    async def run(self):

        msg = await self.receive(timeout=60) # wait for a message

        if msg.get_metadata('performative') == 'infoData':
            data : InfoDashboard
            data = jsonpickle.decode(msg.body)
            data.__str__()

            

            


