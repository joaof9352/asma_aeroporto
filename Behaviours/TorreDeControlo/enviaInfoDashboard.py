from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template

from Templates.infoDashboard import InfoDashboard

import jsonpickle

class EnviaInfoDashboardBehaviour(PeriodicBehaviour): # 3 em 3 segundos

    async def run(self):
        #print("Envia Info Dashboard Behaviour iniciado...")
        
        msgParaGestGares = Message(to=self.agent.get('Gestor De Gares'))  # Instantiate the message
        msgParaGestGares.set_metadata('performative', "requestNumGares")
        await self.send(msgParaGestGares)
        msgDeGestGares = await self.receive(timeout=10)  # esperar a informação do gestor de gares durante 10 segundos
        #print("Received num_gares", msgDeGestGares.body)

        if msgDeGestGares.get_metadata('performative') == 'replyNumGares':
            gares_disp = int(msgDeGestGares.body)

            info = InfoDashboard(self.agent.pistas_disp, gares_disp, self.agent.lista_espera)

            msg = Message(to=self.agent.get('Dashboard'))
            msg.set_metadata("performative", "infoData")
            msg.body = jsonpickle.encode(info)
            await self.send(msg)