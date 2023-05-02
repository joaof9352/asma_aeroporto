from spade import agent

class AviaoAgent(agent.Agent):
    
    #Escolher estas variáveis de acordo com uma lista predefinida de opções

    companhia = ""
    tipo = ""
    origem = ""
    destino = ""
    limite_timeout = 100
    tempo_aterragem = 20
    tempo_descolagem = 20

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
    