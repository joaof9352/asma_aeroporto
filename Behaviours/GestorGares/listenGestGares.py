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

        gestorDeGares = self.agent.get('GestorDeGares')

        if msg.get_metadata('performative') == 'requestNumGares':
            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyNumGares")
            msgParaTorreControlo.body = str(gestorDeGares.gares_disp)
            #print("Gares disponíveis: ", self.agent.gares_disp)

            await self.send(msgParaTorreControlo)
        
        elif msg.get_metadata('performative') == 'incrementGares':
            print("[GEST GARES] Incrementing gares...")
            gestorDeGares.gares_disp = gestorDeGares.gares_disp + 1
            print("[GEST GARES] Gares disponíveis: ", gestorDeGares.gares_disp)

        elif msg.get_metadata('performative') == 'decrementGares':
            print("[GEST GARES] Decrementing gares...")
            gestorDeGares.gares_disp = gestorDeGares.gares_disp - 1
            print("[GEST GARES] Gares disponíveis: ", gestorDeGares.gares_disp)

        elif msg.get_metadata('performative') == 'requestGaresList':
            gestor_de_gares = self.agent.get('GestorDeGares')
            gares = gestor_de_gares.gares

            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyGaresList")
            msgParaTorreControlo.body = jsonpickle.encode(gares)

            await self.send(msgParaTorreControlo)
        elif msg.get_metadata('performative') == 'reserveGare':
            gare = jsonpickle.decode(msg.body)
            gestor_de_gares = self.agent.get('GestorDeGares')
            gestor_de_gares.reserve(gare)

            print(f"[GG] A reservare Gare ({gare.x}, {gare.y})")


            

            


