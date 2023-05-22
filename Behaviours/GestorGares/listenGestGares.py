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

            templateReservaGare : TemplateReservaGare
            templateReservaGare = jsonpickle.decode(msg.body)
            
            aviao = templateReservaGare.getAviao()
            gare = templateReservaGare.getGare()

            gestorDeGares.reserve(gare, aviao)

            if aviao.get_tipo() == "COMERCIAL":
                gestorDeGares.gares_disp_comercial -= 1
                print(f"[GG] A reservare Gare ({gare.x}, {gare.y}) ({gare.type}). Gares disponíveis: {gestorDeGares.gares_disp_comercial}")
            else:
                gestorDeGares.gares_disp_mercadorias -= 1
                print(f"[GG] A reservare Gare ({gare.x}, {gare.y}) ({gare.type}). Gares disponíveis: {gestorDeGares.gares_disp_mercadorias}")
            
            

        elif msg.get_metadata('performative') == 'freeGare':
            aviao = jsonpickle.decode(msg.body)
            gestorDeGares.free_gare(aviao)
            if aviao.get_tipo() == "COMERCIAL":
                gestorDeGares.gares_disp_comercial += 1
                print(f"[GG] A libertar Gare ({aviao.x}, {aviao.y}). Gares disponíveis: {gestorDeGares.gares_disp_comercial}")
            else:
                gestorDeGares.gares_disp_mercadorias += 1
                print(f"[GG] A libertar Gare ({aviao.x}, {aviao.y}). Gares disponíveis: {gestorDeGares.gares_disp_mercadorias}")

        elif msg.get_metadata('performative') == 'getGareAviao':
            aviao = jsonpickle.decode(msg.body)
            gare = gestorDeGares.get_gare_aviao(aviao)
            msgGestGares = Message(to=self.agent.get('Torre De Controlo')) 
            msgGestGares.set_metadata("performative", "replyGareAviao")
            msgGestGares.body = jsonpickle.encode(gare)
            await self.send(msgGestGares)



        self.agent.set("GestorDeGares", gestorDeGares)


            

            


