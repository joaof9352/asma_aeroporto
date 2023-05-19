from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.Aviao import Aviao

class EnderecaPistaBehaviour(PeriodicBehaviour): # 3 em 3 segundos

    async def run(self):
        #print("Endereça Pista Behaviour iniciado...")
        print("A verificar se existem aviões em lista de espera...")
        print(f"Estado: {self.agent.pistas_disp}")
        espera = self.agent.lista_espera
        if len(espera) > 0:
            if self.agent.pistas_disp > 0:
                print("Existem aviões em lista de espera e pistas disponíveis")
                #Comunicar com o gestor de gares
                # msg = Message(to=self.agent.get('Gestor De Gares'))
                # msg.set_metadata("performative", "requestNumGares")
                # await self.send(msg)
                # msgGestGares = await self.receive(timeout=10)

                #if msgGestGares.get_metadata('performative') == 'replyNumGares':
                numGares = self.agent.gares_disp
                self.agent.gares_disp = numGares
                aviao : Aviao
                
                if numGares > 0:
                    # Enviar confirmação para o avião que fez primeiro o pedido, seja este descolar ou aterrar
                    aviao,tipo = espera.pop(0)

                else:
                    avioes_descolar = list(filter(espera, lambda x: x[1] == "descolar")) # caso não haja gares disponíveis, dar prioridade aos aviões que querem descolar
                    if len(avioes_descolar) > 0:
                        aviao, tipo = espera.pop(espera.index(avioes_descolar[0]))
                print(f"A enviar confirmação para o avião {aviao.get_jid()}...")
                await self.__confirm_operation(aviao.get_jid(),tipo)





    async def __confirm_operation(self, aviao_jid, type):
        # se gouver gares disponíveis e pistas disponíveis, decrementar o número de gares disponíveis e pistas disponíveis
        # falta introduzir no corpo da mensagem o número da gare e pista que o avião deve utilizar
        msgParaGestGares = Message(to=self.agent.get('Gestor De Gares'))  # Instantiate the message
        if type == 'aterrar':
            msgParaGestGares.set_metadata("performative", "decrementGares")
            self.agent.gares_disp = self.agent.gares_disp - 1
            self.agent.lista_aterrar.append(aviao_jid.split('@')[0])
        else: 
            msgParaGestGares.set_metadata("performative", "incrementGares")
            self.agent.gares_disp = self.agent.gares_disp + 1
            self.agent.lista_descolar.append(aviao_jid.split('@')[0])
        await self.send(msgParaGestGares)
        print(f"A decrementar o número de pistas disponíveis de {self.agent.pistas_disp} para {self.agent.pistas_disp - 1}")
        self.agent.pistas_disp = self.agent.pistas_disp - 1
        msgParaAviao = Message(to=aviao_jid)  # Instantiate the message
        msgParaAviao.set_metadata("performative", f'confirm_{type}') #confirm_aterrar confirm_descolar
        await self.send(msgParaAviao)
        

