from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle
import time

class EspConfirmAterrarBehaviour(CyclicBehaviour):

    async def run(self):
        print(f"Plane {self.jid} is waiting for confirmation...")
        msg = await self.receive(timeout=self.agent.get('limite_timeout'))  # wait for a message for 10 seconds

        if msg.get_metadata('performative') == 'confirm':
            # se for possível o avião aterrar
            # decrementar o nº de gares disponíveis na torre de controle
            # fazer um sleep que represente o tempo de aterragem
            # talvez definir um tempo limite até ele levantar voo outra vez
            time.sleep(self.agent.get('tempo_aterragem'))
            print(f"O Avião {self.jid} aterrou...")
        elif msg.get_metadata('performative') == 'wait':
            # se não for possível o avião aterrar e o nº de aviões em espera for menor que o limite
            # incrementar o nº de aviões em espera
            # talvez inserior o jid do avião numa queue na torre de controlo para que este possa depois ser chamado para aterrar novamente
            # talvez ter um behaviour que fique à espera de uma mensagem de confirmação
            time.sleep(5) # Random sleep time
            # enviar mensagem para a torre de controlo a informar que aterrou para que esta possa disponibilizar a pista
        elif msg.get_metadata('performative') == 'full':
            # se não for possível o avião aterrar e o nº de aviões em espera for maior ou igual ao limite
            # avião poderá sair do sistema
            print(f"O Avião {self.jid} vai aterrar noutro aeroporto...")
            self.kill(exit_code=10)

