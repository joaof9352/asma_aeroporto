from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.Aviao import Aviao
from Templates.TemplateReservaGare import TemplateReservaGare

class ListenGestGaresBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=60)  # wait for a message

        if not msg:
            pass

        gestorDeGares = self.agent.get('GestorDeGares')

        if msg.get_metadata('performative') == 'requestGaresList':
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
                print(f"[GG] A reservar Gare ({gare.x}, {gare.y}) ({gare.type}). Numero de gares comerciais disponíveis: {gestorDeGares.gares_disp_comercial}")
            else:
                gestorDeGares.gares_disp_mercadorias -= 1
                print(f"[GG] A reservar Gare ({gare.x}, {gare.y}) ({gare.type}). Numero de gares de mercadorias disponíveis: {gestorDeGares.gares_disp_mercadorias}")
            
            

        elif msg.get_metadata('performative') == 'freeGare':
            aviao = jsonpickle.decode(msg.body)
            gestorDeGares.free_gare(aviao)
            if aviao.get_tipo() == "COMERCIAL":
                gestorDeGares.gares_disp_comercial += 1
                print(f"[GG] A libertar Gare ({aviao.x}, {aviao.y}). Numero de gares comerciais disponíveis: {gestorDeGares.gares_disp_comercial}")
            else:
                gestorDeGares.gares_disp_mercadorias += 1
                print(f"[GG] A libertar Gare ({aviao.x}, {aviao.y}). Numero de gares de mercadorias disponíveis: {gestorDeGares.gares_disp_mercadorias}")

        elif msg.get_metadata('performative') == 'getGareAviao':
            aviao = jsonpickle.decode(msg.body)
            gare = gestorDeGares.get_gare_aviao(aviao)
            msgGestGares = Message(to=self.agent.get('Torre De Controlo')) 
            msgGestGares.set_metadata("performative", "replyGareAviao")
            msgGestGares.body = jsonpickle.encode(gare)
            await self.send(msgGestGares)

        elif msg.get_metadata('performative') == 'getNumGares':
            msgParaTorreControlo = Message(to=self.agent.get('Torre De Controlo'))  # Instantiate the message
            msgParaTorreControlo.set_metadata("performative", "numGares")
            msgParaTorreControlo.body = f'{gestorDeGares.gares_disp_comercial},{gestorDeGares.gares_disp_mercadorias}'
            await self.send(msgParaTorreControlo)



        self.agent.set("GestorDeGares", gestorDeGares)


            

            


