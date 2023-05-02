from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

class ListenTorreControloBehaviour(CyclicBehaviour):

    async def run(self):
        
        msg = await self.receive()  # wait for a message

        if msg.get_metadata('requestLanding'):
            # se receber um pedido de um avião para aterrar
            # verificar se existem gares disponíveis e pistas disponíveis
            msgParaGestGares = Message(to=self.agent.get('Gestor de Gares'))  # Instantiate the message
            msgParaGestGares.set_metadata("performative", "requestNumGares")
            await self.send(msgParaGestGares)
            msgDeGestGares = await self.receive(timeout=10)  # wait for a message for 10 seconds
            gares_disp = msgDeGestGares.body
            if gares_disp > 0 and self.agent.get('pistas_disp') > 0:
                # se gouver gares disponíveis e pistas disponíveis, decrementar o número de gares disponíveis e pistas disponíveis
                msgParaAviao = Message(to=msg.sender)  # Instantiate the message
                msgParaAviao.set_metadata("performative", "confirm")
                # falta introduzir no corpo da mensagem o número da gare e pista que o avião deve utilizar
                await self.send(msgParaAviao)
                msgParaGestGares = Message(to=self.agent.get('Gestor de Gares'))  # Instantiate the message
                msgParaGestGares.set_metadata("performative", "decrementGares")
                await self.send(msgParaGestGares)
                self.agent.set('pistas_disp', self.agent.get('pistas_disp') - 1)
            else:
                # Se o avião não puder aterrar, por falta de gares ou de pistas, colocar ou não em fila de espera, caso o limite de aviões em espera seja atingido
                espera = self.agent.get('esperaAterrar')
                if len(espera) < self.agent.get('limite_espera'):
                    espera.append(msg.sender)
                    msgParaAviao = Message(to=msg.sender)
                    msgParaAviao.set_metadata("performative", "wait")
                    await self.send(msgParaAviao)
                else:
                    msgParaAviao = Message(to=msg.sender)
                    msgParaAviao.set_metadata("performative", "full")
                    await self.send(msgParaAviao)
        elif msg.get_metadata('performative') == 'requestTakeOff':
            pass
        elif msg.get_metadata('performative') == 'requestData':
            pass

        


        

        
