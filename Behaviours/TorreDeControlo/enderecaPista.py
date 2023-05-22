from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.template import Template
import random
import jsonpickle

from Templates.Aviao import Aviao
from Templates.TorreDeControlo import TorreDeControlo
from Templates.Pista import Pista
from Templates.Gare import Gare
from Templates.TemplateReservaGare import TemplateReservaGare

import asyncio

class EnderecaPistaBehaviour(PeriodicBehaviour): # 3 em 3 segundos

    async def run(self):
        #print("Endereça Pista Behaviour iniciado...")
        torreDeControlo : TorreDeControlo = self.agent.get('TorreDeControlo')
        #print("A verificar se existem aviões em lista de espera...")
        #print(f"Estado: {torreDeControlo.pistas_disp}")
        espera = torreDeControlo.lista_espera
        if len(espera) > 0:
            if torreDeControlo.pistas_disp > 0:
                #print("Existem aviões em lista de espera e pistas disponíveis")
                aviao : Aviao
                aviao,tipo = espera[0]
                #print(f'{aviao.get_jid()} + {aviao.get_tipo()}')

                if aviao.get_tipo() == 'COMERCIAL':
                    numGares = torreDeControlo.gares_disp_comercial
                else:
                    numGares = torreDeControlo.gares_disp_mercadorias

                #print(f'Num Gares {numGares}')

                if numGares > 0:
                    # Enviar confirmação para o avião que fez primeiro o pedido, seja este descolar ou aterrar
                    aviao,tipo = espera.pop(0)
                    print(f"A enviar confirmação para o avião {aviao.get_jid()}...")
                    await self.__confirm_operation(torreDeControlo, aviao, tipo, numGares)
                else:
                    #print("Debugs 1")
                    avioes_descolar = list(filter(lambda x: x[1] == "descolar" and x[0].get_tipo() == aviao.get_tipo(), espera)) # caso não haja gares disponíveis, dar prioridade aos aviões que querem descolar
                    if len(avioes_descolar) > 0:
                        aviao, tipo = espera.pop(espera.index(avioes_descolar[0]))
                        print(f"A enviar confirmação para o avião {aviao.get_jid()}...")
                        await self.__confirm_operation(torreDeControlo, aviao, tipo, numGares)

        self.agent.set("TorreDeControlo", torreDeControlo)

    async def __confirm_operation(self, torreDeControlo, aviao, type, numGares):
        # se gouver gares disponíveis e pistas disponíveis, decrementar o número de gares disponíveis e pistas disponíveis
        # falta introduzir no corpo da mensagem o número da gare e pista que o avião deve utilizar
        msgParaGestGares = Message(to=self.agent.get('Gestor De Gares'))  # Instantiate the message
        if type == 'aterrar':
            # TODO: Isto é suposto estar aqui?
            #msgParaGestGares.set_metadata("performative", "decrementGares")

            msg = Message(to=self.agent.get('Gestor De Gares'))
            msg.set_metadata("performative", "requestGaresList")
            await self.send(msg)

            msgGestGares = await self.receive(timeout=20)
            while msgGestGares.get_metadata('performative') != 'replyGaresList':
                msgGestGares = await self.receive(timeout=20)

            if msgGestGares.get_metadata('performative') == 'replyGaresList':
                gares = list(jsonpickle.decode(msgGestGares.body))
                #print("GARES:", gares)
                
                best_pista : Pista
                best_gare : Gare
                print(f'Numero de gares disponiveis do tipo {aviao.get_tipo()}: {numGares}')
                best_pista, best_gare = torreDeControlo.getBestPista(gares, aviao)

                #print(f'AAAAAAAAAAAAAAAAAAAAAAAAAA -> {best_pista, best_gare}')

                if best_gare is not None and best_pista is not None:
                    #Reserva gare
                    best_pista.assign_plane(aviao) # reservar a pista para o avião. Quando o avião confirmar a aterragem é preciso libertar a pista.

                    # Reservar gare
                    msgGestGares = Message(to=self.agent.get('Gestor De Gares'))
                    msgGestGares.set_metadata("performative", "reserveGare")
                    templateReservaGare = TemplateReservaGare(aviao, best_gare)
                    msgGestGares.body = jsonpickle.encode(templateReservaGare)

                    await self.send(msgGestGares)
                    
                    if aviao.get_tipo() == 'COMERCIAL':
                        torreDeControlo.gares_disp_comercial -= 1
                    else:
                        torreDeControlo.gares_disp_mercadorias -= 1

                    torreDeControlo.lista_aterrar.append(aviao.get_jid().split('@')[0])
                    print(f'Adicionado o {aviao.get_jid().split("@")[0]} à lista de avião a aterrar')
        else:
            # obtenção da gare em que este avião se encontra
            gareAviaoMsg = Message(to=self.agent.get('Gestor De Gares'))
            gareAviaoMsg.set_metadata("performative", "getGareAviao")
            gareAviaoMsg.body = jsonpickle.encode(aviao)
            await self.send(gareAviaoMsg)
            #print("DEBUG ENVIO GET GARE AVIAO AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            
            gareAviaoMsg = await self.receive(timeout=20)

            while gareAviaoMsg.get_metadata('performative') != 'replyGareAviao':
                gareAviaoMsg = await self.receive(timeout=20)

            if gareAviaoMsg.get_metadata('performative') == 'replyGareAviao':
                #print("DEBUG CENAS")
                gare : Gare = jsonpickle.decode(gareAviaoMsg.body)
                # obtenção da pista mais próxima desta gare que esteja disponível
                #print("HELLO HELLO GARE: ", gare)
                best_pista = torreDeControlo.get_best_pista_descolagem(gare)
                # reservar a pista para o avião. Quando o avião confirmar a descolagem é preciso libertar a pista.
                best_pista.assign_plane(aviao)

                msgParaGestGares.set_metadata("performative", "freeGare")
                msgParaGestGares.body = jsonpickle.encode(aviao) # ao enviar o avião no corpo da mensagem, o gestor de gares poderá procurar qual a gare em que o avião se encontra e libertá-la
                if aviao.get_tipo() == 'COMERCIAL':
                    torreDeControlo.gares_disp_comercial += 1
                else:
                    torreDeControlo.gares_disp_mercadorias += 1
                torreDeControlo.lista_descolar.append(aviao.get_jid().split('@')[0])
        await self.send(msgParaGestGares)
        #print(f"A decrementar o número de pistas disponíveis de {torreDeControlo.pistas_disp} para {torreDeControlo.pistas_disp - 1}")
        torreDeControlo.pistas_disp = torreDeControlo.pistas_disp - 1
        msgParaAviao = Message(to=aviao.get_jid())  # Instantiate the message
        msgParaAviao.set_metadata("performative", f'confirm_{type}') #confirm_aterrar confirm_descolar
        self.agent.set('TorreDeControlo', torreDeControlo)
        await self.send(msgParaAviao)

