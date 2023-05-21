from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.Aviao import Aviao
from Templates.TemplateReservaGare import TemplateReservaGare

class ListenGestGaresBehaviour(CyclicBehaviour):

    async def run(self):
        print("Listen Gest Gares Behaviour iniciado...")
        msg = await self.receive(timeout=60)  # wait for a message

        #print("Message in Gest Gares ", msg.body)

        if not msg:
            pass

        msgGestGares = Message(to=self.agent.get('Gestor De Gares')) 
        #msgGestGares.set_metadata("performative", "")

        gestorDeGares = self.agent.get('GestorDeGares')

        if msg.get_metadata('performative') == 'requestNumGares':
            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyNumGares")
            msgParaTorreControlo.body = str(gestorDeGares.gares_disp)
            #print("Gares disponíveis: ", self.agent.gares_disp)

            await self.send(msgParaTorreControlo)

        elif msg.get_metadata('performative') == 'requestGaresList':
            #gestor_de_gares = self.agent.get('GestorDeGares')
            gares = gestorDeGares.listaGares

            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "replyGaresList")
            msgParaTorreControlo.body = jsonpickle.encode(gares)

            await self.send(msgParaTorreControlo)
        elif msg.get_metadata('performative') == 'reserveGare':
            gestorDeGares.gares_disp -= 1

            templateReservaGare : TemplateReservaGare
            templateReservaGare = jsonpickle.decode(msg.body)
            
            aviao = templateReservaGare.getAviao()
            gare = templateReservaGare.getGare()
            
            gestorDeGares.reserve(gare, aviao)

            print(f"[GG] A reservare Gare ({gare.x}, {gare.y}). Gares disponíveis: {gestorDeGares.gares_disp}")

        elif msg.get_metadata('performative') == 'freeGare':
            gestorDeGares.gares_disp += 1
            aviao = jsonpickle.decode(msg.body)
            gestorDeGares.free_gare(aviao)
            print(f"[GG] A libertar Gare ({aviao.x}, {aviao.y}). Gares disponíveis: {gestorDeGares.gares_disp}")

        elif msg.get_metadata('performative') == 'getGareAviao':
            aviao = jsonpickle.decode(msg.body)
            gare = gestorDeGares.get_gare_aviao(aviao)
            msgGestGares.set_metadata("performative", "replyGareAviao")
            msgGestGares.body = jsonpickle.encode(gare)
            await self.send(msgGestGares)
            


        self.agent.set("GestorDeGares", gestorDeGares)


            

            


