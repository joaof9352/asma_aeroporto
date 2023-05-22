from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle
import time
import asyncio

from Behaviours.Aviao.vontadeDescolar import VontadeDescolarBehaviour
from Templates.Aviao import Aviao


class EspConfirmacaoBehaviour(CyclicBehaviour):

    async def __send_msg(self, agent, performative, body=None):
        msg = Message(to=agent)  # Instantiate the message
        msg.set_metadata("performative", performative)
        if body is not None:
            msg.body = body
        await self.send(msg)

    async def run(self):
        
        aviao : Aviao
        aviao = self.agent.get('Aviao')
        print(f"[{self.agent.jid} ({aviao.get_tipo()})] Plane {self.agent.jid} is waiting for confirmation...")

        
        msg = await self.receive(timeout=aviao.get_limite_timeout())  # wait for a message for 10 seconds

        if not msg and self.agent.get('quer_aterrar'):
            msg = Message(to=self.agent.get('Torre De Controlo'))  # Instanciar a mensagem para a torre de controlo
            msg.set_metadata("performative", "cancelLanding")
            await self.send(msg)
            self.kill(exit_code=10)
        elif not msg and not self.agent.get('quer_aterrar'):
            pass
        elif msg.get_metadata('performative') == 'confirm_descolar':
            # se for possível o avião aterrar
            # decrementar o nº de gares disponíveis na torre de controle
            # fazer um sleep que represente o tempo de aterragem
            # talvez definir um tempo limite até ele levantar voo outra vez
            print(f"[{aviao.get_jid()}] O Avião {aviao.get_jid()} recebeu confirmação para descolar...")
            await asyncio.sleep(self.agent.get('Aviao').get_tempo_descolagem())
            print(f"[{aviao.get_jid()}] O Avião {aviao.get_jid()} descolou...")
            await self.__send_msg(self.agent.get('Torre De Controlo'), "planeTookOff", jsonpickle.encode(self.agent.get('Aviao')))
            self.kill(exit_code=10)

        elif msg.get_metadata('performative') == 'confirm_aterrar':
            # se for possível o avião aterrar
            # decrementar o nº de gares disponíveis na torre de controle
            # fazer um sleep que represente o tempo de aterragem
            # talvez definir um tempo limite até ele levantar voo outra vez
            print(f"[{aviao.get_jid()} O Avião {aviao.get_jid()}] recebeu confirmação para aterrar...")
            self.agent.set('quer_aterrar', True)
            
            await asyncio.sleep(aviao.get_tempo_aterragem())
            print(f"[{aviao.get_jid()} ({aviao.get_tipo()})] O Avião {aviao.get_jid()} aterrou...")
            
            await self.__send_msg(self.agent.get('Torre De Controlo'), "planeLanded", jsonpickle.encode(self.agent.get('Aviao')))
            self.agent.set('quer_aterrar', False)

            # Adiciona e inicia o behaviour de descolagem
            
            await asyncio.sleep(10) # depois poderá ser um tempo aleatório

            b = VontadeDescolarBehaviour()
            self.agent.add_behaviour(b)
            

        elif msg.get_metadata('performative') == 'full':
            # se não for possível o avião aterrar e o nº de aviões em espera for maior ou igual ao limite
            # avião poderá sair do sistema
            print(f"[{aviao.get_jid()} ({aviao.get_tipo()})] O Avião {aviao.get_jid()} vai aterrar noutro aeroporto...")
            self.kill(exit_code=10)