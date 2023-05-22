from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from Templates.infoDashboard import InfoDashboard
from Templates.Aviao import Aviao

import random
import jsonpickle


class ListenTorreControloBehaviour(CyclicBehaviour):


    async def __request_landing(self, torreDeControlo, msg):
        # se receber um pedido de um avião para aterrar
        # verificar se existem gares disponíveis e pistas disponíveis
        print("[TC] Recebi pedido para aterrar do aviao", msg.sender)

        if torreDeControlo.pistas_disp == 0:
            print("[TC] Não há gares ou pistas disponíveis")
            await self.__deny_landing(torreDeControlo, msg)
        else:
            print("[TC] Há gares e pistas disponíveis")
            espera = torreDeControlo.lista_espera
            torreDeControlo.lista_espera = espera + [(jsonpickle.decode(msg.body), "aterrar")]

    async def __deny_landing(self, torreDeControlo, msg):
        # Se o avião não puder aterrar, por falta de gares ou de pistas, colocar ou não em fila de espera, caso o limite de aviões em espera seja atingido
        espera = torreDeControlo.lista_espera
        num_avioes_espera = len(list(filter(lambda x: x[1] == "aterrar", espera)))
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        if num_avioes_espera < torreDeControlo.limite_espera: # Colocar em lista de espera
            torreDeControlo.lista_espera = espera + [(aviao, "aterrar")]
            self.agent.set('TorreDeControlo', torreDeControlo)
        else:
            msgParaAviao = Message(to=aviao.get_jid()) #Enviar o avião para outro aeroporto
            msgParaAviao.set_metadata("performative", "full")
            await self.send(msgParaAviao)
        
 
    async def __request_take_off(self, torreDeControlo, msg):
        # Verificar se há pistas. Se não houver, verificar se há gares. Se não houver, avião ganha prioridade, senão entra para a fila de espera
        
        espera = torreDeControlo.lista_espera
        torreDeControlo.lista_espera = espera + [(jsonpickle.decode(msg.body), "descolar")]
 
    async def __cancelLanding(self, torreDeControlo, msg):
        #Retirar da lista de espera
        print("[TC] A cancelar pedido de aterragem do aviao", msg.sender)
        aviao_jid = msg.sender
        espera = torreDeControlo.lista_espera
        torreDeControlo.lista_espera = [x for x in espera if str(x[0].get_jid()) != str(aviao_jid)]

    async def __done_Landing(self, torreDeControlo, msg):
        print(f"[TC] A incrementar pistas disponíveis de {torreDeControlo.pistas_disp} para {torreDeControlo.pistas_disp + 1}")
        torreDeControlo.pistas_disp = torreDeControlo.pistas_disp + 1
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        torreDeControlo.landing_completed(aviao)
        torreDeControlo.lista_aterrar.remove(aviao.get_jid().split("@")[0])

    async def __done_TakeOff(self, torreDeControlo, msg):
        print(f"[TC] A incrementar pistas disponíveis de {torreDeControlo.pistas_disp} para {torreDeControlo.pistas_disp + 1}")
        torreDeControlo.pistas_disp = torreDeControlo.pistas_disp + 1
        aviao : Aviao
        aviao = jsonpickle.decode(msg.body)
        torreDeControlo.lista_descolar.remove(aviao.get_jid().split("@")[0])
        torreDeControlo.landing_completed(aviao)
        

    async def run(self):

        msg = await self.receive(timeout=60)  # wait for a message        

        if not msg:
            pass

        torreDeControlo = self.agent.get('TorreDeControlo')

        if msg.get_metadata('performative') == 'requestLanding':
            await self.__request_landing(torreDeControlo, msg)
        elif msg.get_metadata('performative') == 'requestTakeOff':
            await self.__request_take_off(torreDeControlo, msg)
        elif msg.get_metadata('performative') == 'updateGares':
            await self.__updateGares(torreDeControlo, msg)
        elif msg.get_metadata('performative') == 'cancelLanding':
            await self.__cancelLanding(torreDeControlo, msg)
        elif msg.get_metadata('performative') == 'planeLanded':
            await self.__done_Landing(torreDeControlo, msg)
        elif msg.get_metadata('performative') == 'planeTookOff':
            await self.__done_TakeOff(torreDeControlo, msg)
        
        self.agent.set('TorreDeControlo', torreDeControlo)