from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

class EnderecaPistaBehaviour(PeriodicBehaviour): # 3 em 3 segundos

    async def run(self):
        espera = self.agent.get('lista_espera')
        if len(espera) > 0:
            if self.agent.get('pistas_disp') > 0:
                #Comunicar com o gestor de gares
                msg = Message(to=self.agent.get('Gestor de Gares'))
                msg.set_metadata("performative", "requestNumGares") 
                await self.send(msg)
                numGares = msg.body
                if numGares > 0:
                    # Enviar confirmação para o avião
                    aviao = espera.pop(0)
                else:
                    avioes_descolar = list(filter(espera, lambda x: x[1] == "descolar"))
                    if len(avioes_descolar) > 0:
                        aviao = espera.pop(espera.index(avioes_descolar[0]))
                
                self.__confirm_operation(aviao[0],aviao[1])


    async def __confirm_operation(self, aviao_jid, type):
        # se gouver gares disponíveis e pistas disponíveis, decrementar o número de gares disponíveis e pistas disponíveis
        msgParaAviao = Message(to=aviao_jid)  # Instantiate the message
        msgParaAviao.set_metadata("performative", f'confirm_{type}') #confirm_aterrar confirm_descolar
        # falta introduzir no corpo da mensagem o número da gare e pista que o avião deve utilizar
        await self.send(msgParaAviao)
        msgParaGestGares = Message(to=self.agent.get('Gestor de Gares'))  # Instantiate the message
        if type == 'aterrar':
            msgParaGestGares.set_metadata("performative", "decrementGares")
        else: 
            msgParaGestGares.set_metadata("performative", "incrementGares")
        await self.send(msgParaGestGares)
        self.agent.set('pistas_disp', self.agent.get('pistas_disp') - 1)
 

