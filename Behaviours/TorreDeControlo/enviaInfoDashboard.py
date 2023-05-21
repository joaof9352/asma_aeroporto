from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template

from Templates.infoDashboard import InfoDashboard

import jsonpickle

class EnviaInfoDashboardBehaviour(PeriodicBehaviour): # 3 em 3 segundos

    async def run(self):
        #print("Envia Info Dashboard Behaviour iniciado...")
        
        torreDeControlo = self.agent.get('TorreDeControlo')
        gares_disp_comercial = torreDeControlo.gares_disp_comercial
        gares_disp_mercadorias = torreDeControlo.gares_disp_mercadorias

        info = InfoDashboard(torreDeControlo.pistas_disp, gares_disp_comercial, gares_disp_mercadorias, torreDeControlo.lista_espera, 
                            torreDeControlo.lista_aterrar, torreDeControlo.lista_descolar)

        msg = Message(to=self.agent.get('Dashboard'))
        msg.set_metadata("performative", "infoData")
        msg.body = jsonpickle.encode(info)
        await self.send(msg)