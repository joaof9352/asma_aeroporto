from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from Templates.infoDashboard import InfoDashboard
from Templates.Aviao import Aviao

import random
import jsonpickle


class ListenTorreControloBehaviour(CyclicBehaviour):

    async def __request_landing(self, msg):
        # se receber um pedido de um avião para aterrar
        # verificar se existem gares disponíveis e pistas disponíveis
        msgParaGestGares = Message(to=self.agent.get('Gestor de Gares'))  # Instantiate the message
        msgParaGestGares.set_metadata("performative", "requestNumGares")
        await self.send(msgParaGestGares)
        msgDeGestGares = await self.receive(timeout=10)  # esperar a informação do gestor de gares durante 10 segundos
        gares_disp = msgDeGestGares.body
        
        if gares_disp == 0 or self.agent.get('pistas_disp') == 0:
            self.__deny_landing(msg)
        else:
            espera = self.agent.get('lista_espera')
            self.agent.set('lista_espera', espera + [(msg.sender, "aterrar")])

    async def __deny_landing(self, msg):
        # Se o avião não puder aterrar, por falta de gares ou de pistas, colocar ou não em fila de espera, caso o limite de aviões em espera seja atingido
        espera = self.agent.get('lista_espera')
        num_avioes_espera = len(list(filter(espera, lambda x: x[1] == "aterrar")))
        if num_avioes_espera < self.agent.get('limite_espera'): # Colocar em lista de espera
            self.agent.set('lista_espera', espera + [(jsonpickle.decode(msg.body), "aterrar")])
            msgParaAviao = Message(to=msg.sender)
            msgParaAviao.set_metadata("performative", "wait")
            await self.send(msgParaAviao)
        else:
            msgParaAviao = Message(to=msg.sender) #Enviar o avião para outro aeroporto
            msgParaAviao.set_metadata("performative", "full")
            await self.send(msgParaAviao)
 
    async def __request_take_off(self, msg):
        # Verificar se há pistas. Se não houver, verificar se há gares. Se não houver, avião ganha prioridade, senão entra para a fila de espera
        pistas_disp = self.agent.get('pistas_disp')
        if pistas_disp > 0:
            espera = self.agent.get('lista_espera')
            self.agent.set('lista_espera', espera + [(jsonpickle.decode(msg.body), "descolar")])
        else:
            msgParaAviao = Message(to=msg.sender)
            msgParaAviao.set_metadata("performative", "wait")
            await self.send(msgParaAviao)

    async def __request_data(self, msg):
        lista_espera = self.agent.get('lista_espera')
        num_pistas_disp = self.agent.get('pistas_disp')

        msgParaGestGares = Message(to=msg.sender)  # Instantiate the message
        msgParaGestGares.set_metadata("performative", "requestNumGares")
        await self.send(msgParaGestGares)
        msgDeGestGares = await self.receive(timeout=10)  # esperar a informação do gestor de gares durante 10 segundos
        num_gares_disp = msgDeGestGares.body

        infoParaDashboard = InfoDashboard(num_pistas_disp, num_gares_disp, lista_espera)

        msg = Message(to=self.agent.get('Gestor De Gares'))
        msg.set_metadata('performative', '')

    async def __update_gares(self, msg):
        pass

    async def __cancelLanding(self, msg):
        #Retirar da lista de espera
        aviao_jid = msg.sender
        espera = self.agent.get('lista_espera')
        x = list(filter(espera, lambda x: x[0].get_jid() != aviao_jid)) #Retirar o avião da lista de espera
        espera.remove((aviao_jid,"aterrar"))
        self.agent.set('lista_espera', espera)

    async def __done_Landing(self):
        self.agent.set('pistas_disp', self.agent.get('pistas_disp') + 1)

    async def run(self):
        
        msg = await self.receive()  # wait for a message

        if msg.get_metadata('performative') == 'requestLanding':
            self.__request_landing(msg)
        elif msg.get_metadata('performative') == 'requestTakeOff':
            self.__request_take_off(msg)
        elif msg.get_metadata('performative') == 'requestData':
            self.__request_data(msg)
        elif msg.get_metadata('performative') == 'updateGares':
            self.__updateGares(msg)
        elif msg.get_metadata('performative') == 'cancelLanding':
            self.__cancelLanding(msg)
        elif msg.get_metadata('performative') == 'aterragem_concluida':
            self.__done_Landing()


        

        
