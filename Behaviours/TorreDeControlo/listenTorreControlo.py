from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from Templates.infoDashboard import InfoDashboard
from Templates.Aviao import Aviao

import random
import jsonpickle


class ListenTorreControloBehaviour(CyclicBehaviour):

    async def request_num_gares(self):
        msgParaGestGares = Message(to=self.agent.get('Gestor De Gares'))  # Instantiate the message
        msgParaGestGares.set_metadata("performative", "requestNumGares")
        await self.send(msgParaGestGares)
        msgDeGestGares = await self.receive(timeout=10)  # esperar a informação do gestor de gares durante 10 segundos

        return msgDeGestGares


    async def __request_landing(self, msg):
        # se receber um pedido de um avião para aterrar
        # verificar se existem gares disponíveis e pistas disponíveis
        print("Recebi pedido para aterrar do aviao", msg.sender)
        msgDeGestGares = await self.request_num_gares()
        if msgDeGestGares.get_metadata('performative') == 'replyNumGares':
            gares_disp = msgDeGestGares.body
            
            if gares_disp == 0 or self.agent.pistas_disp == 0:
                print("Não há gares ou pistas disponíveis")
                await self.__deny_landing(msg)
            else:
                print("Há gares e pistas disponíveis")
                espera = self.agent.lista_espera
                self.agent.lista_espera = espera + [(jsonpickle.decode(msg.body), "aterrar")]

    async def __deny_landing(self, msg):
        # Se o avião não puder aterrar, por falta de gares ou de pistas, colocar ou não em fila de espera, caso o limite de aviões em espera seja atingido
        espera = self.agent.lista_espera
        num_avioes_espera = len(list(filter(lambda x: x[1] == "aterrar", espera)))
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        if num_avioes_espera < self.agent.limite_espera: # Colocar em lista de espera
            self.agent.lista_espera = espera + [(aviao, "aterrar")]
            #msgParaAviao = Message(to=aviao.get_jid())
            #msgParaAviao.set_metadata("performative", "wait")
            #await self.send(msgParaAviao)
        else:
            msgParaAviao = Message(to=aviao.get_jid()) #Enviar o avião para outro aeroporto
            msgParaAviao.set_metadata("performative", "full")
            await self.send(msgParaAviao)
 
    async def __request_take_off(self, msg):
        # Verificar se há pistas. Se não houver, verificar se há gares. Se não houver, avião ganha prioridade, senão entra para a fila de espera
        
        pistas_disp = self.agent.pistas_disp
        espera = self.agent.lista_espera
        self.agent.lista_espera = espera + [(jsonpickle.decode(msg.body), "descolar")]
        #msgParaAviao = Message(to=jsonpickle.decode(msg.body).get_jid())
        #msgParaAviao.set_metadata("performative", "wait")
        #await self.send(msgParaAviao)

    async def __update_gares(self, msg):
        pass

    async def __cancelLanding(self, msg):
        #Retirar da lista de espera
        aviao_jid = msg.sender
        espera = self.agent.lista_espera
        x = list(filter(lambda x: x[0].get_jid().split("@")[0] != aviao_jid, espera)) #Retirar o avião da lista de espera
        self.agent.lista_espera = x

    async def __done_Landing(self, msg):
        print(f"A incrementar pistas disponíveis de {self.agent.pistas_disp} para {self.agent.pistas_disp + 1}")
        self.agent.pistas_disp = self.agent.pistas_disp + 1
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        self.agent.lista_aterrar.remove(aviao.get_jid().split("@")[0])

    async def __done_TakeOff(self, msg):
        print(f"A incrementar pistas disponíveis de {self.agent.pistas_disp} para {self.agent.pistas_disp + 1}")
        self.agent.pistas_disp = self.agent.pistas_disp + 1
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        self.agent.lista_descolar.remove(aviao.get_jid().split("@")[0])

    async def run(self):
        #print("Listen Torre de Controlo Behaviour iniciado...")

        msg = await self.receive(timeout=60)  # wait for a message

        #print("teste after await receive listen torre de controlo")

        if not msg:
            pass

        if msg.get_metadata('performative') == 'requestLanding':
            await self.__request_landing(msg)
        elif msg.get_metadata('performative') == 'requestTakeOff':
            await self.__request_take_off(msg)
        elif msg.get_metadata('performative') == 'updateGares':
            await self.__updateGares(msg)
        elif msg.get_metadata('performative') == 'cancelLanding':
            await self.__cancelLanding(msg)
        elif msg.get_metadata('performative') == 'planeLanded':
            await self.__done_Landing(msg)
        elif msg.get_metadata('performative') == 'planeTookOff':
            await self.__done_TakeOff(msg)


        

        
