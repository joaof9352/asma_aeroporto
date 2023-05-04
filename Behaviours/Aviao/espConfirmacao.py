from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle
import time

class EspConfirmacaoBehaviour(CyclicBehaviour):

    async def __send_msg(self, agent, performative):
        msg = Message(to=agent)  # Instantiate the message
        msg.set_metadata("performative", performative)
        await self.send(msg)

    async def run(self):
        print(f"Plane {self.jid} is waiting for confirmation...")
        msg = await self.receive(timeout=self.agent.get('limite_timeout'))  # wait for a message for 10 seconds

        if not msg:
            msg = Message(to=self.agent.get('Torre de Controlo'))  # Instantiate the message
            msg.set_metadata("performative", "cancelLanding")
            await self.send(msg)
            self.kill(exit_code=10)

        if msg.get_metadata('performative') == 'confirm_descolar':
            # se for possível o avião aterrar
            # decrementar o nº de gares disponíveis na torre de controle
            # fazer um sleep que represente o tempo de aterragem
            # talvez definir um tempo limite até ele levantar voo outra vez
            time.sleep(self.agent.get('tempo_descolagem'))
            print(f"O Avião {self.jid} aterrou...")
            await self.__send_msg(self.jid, "aterragem_concluida")
        elif msg.get_metadata('performative') == 'confirm_aterrar':
            # se for possível o avião aterrar
            # decrementar o nº de gares disponíveis na torre de controle
            # fazer um sleep que represente o tempo de aterragem
            # talvez definir um tempo limite até ele levantar voo outra vez
            time.sleep(self.agent.get('tempo_aterragem'))
            print(f"O Avião {self.jid} aterrou...")
        elif msg.get_metadata('performative') == 'full':
            # se não for possível o avião aterrar e o nº de aviões em espera for maior ou igual ao limite
            # avião poderá sair do sistema
            print(f"O Avião {self.jid} vai aterrar noutro aeroporto...")
            self.kill(exit_code=10)

