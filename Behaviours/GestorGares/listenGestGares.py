from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.Aviao import Aviao

class ListenGestGaresBehaviour(CyclicBehaviour):

    async def run(self):
        print("Listen Gest Gares Behaviour iniciado...")
        msg = await self.receive(timeout=60)  # wait for a message

        #print("Message in Gest Gares ", msg.body)

        if not msg:
            pass

        elif msg.get_metadata('performative') == 'requestNumGares':
            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyNumGares")
            msgParaTorreControlo.body = str(self.agent.gares_disp)
            #print("Gares disponíveis: ", self.agent.gares_disp)

            await self.send(msgParaTorreControlo)
        
        elif msg.get_metadata('performative') == 'incrementGares':
            print("[GEST GARES] Incrementing gares...")
            self.agent.gares_disp = self.agent.gares_disp + 1
            print("[GEST GARES] Gares disponíveis: ", self.agent.gares_disp)

        elif msg.get_metadata('performative') == 'decrementGares':
            print("[GEST GARES] Decrementing gares...")
            self.agent.gares_disp = self.agent.gares_disp - 1
            print("[GEST GARES] Gares disponíveis: ", self.agent.gares_disp)

            


