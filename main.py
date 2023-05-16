from spade import agent, quit_spade
from Agents import AviaoAgent, TorreControloAgent, DashboardAgent, GestorDeGaresAgent
import random
import time

XMPP_SERVER = 'legion'
PASSWORD = 'openfireASMA'

MAX_AVIOES = 20  # limit number of taxis



def main():
    i = 0

    # Initialize list to save all active Agents in list
    lista_agentes_avioes = []

    torre_controlo = TorreControloAgent("torre@localhost", "1234")
    gestor_de_gares = GestorDeGaresAgent("gestor_de_gares@localhost", "1234")
    dashboard = DashboardAgent("dashboard@localhost", "1234")

    # Fazer set dos agentes para que possam comunicar entre si

    torre_controlo.set('Gestor De Gares', gestor_de_gares.jid)
    torre_controlo.set('Dashboard', dashboard.jid)

    gestor_de_gares.set('Torre De Controlo', torre_controlo.jid)
    gestor_de_gares.set('Dashboard', dashboard.jid)

    dashboard.set('Torre De Controlo', torre_controlo.jid)
    dashboard.set('Gestor De Gares', gestor_de_gares.jid)

    # Inicializar os agentes principais (torre de controlo, gestor de gares e dashboard)

    torre_controlo.start()
    gestor_de_gares.start()
    dashboard.start()

    while i < MAX_AVIOES:
        random_time = random.randint(1, 10)
        aviaoAgent = AviaoAgent(f"plane{i}@localhost", "1234")
        aviaoAgent.set('Torre De Controlo', torre_controlo.jid) # Fazer com que o avião conheça a torre de controlo, para que possa comunicar com ela
        time.sleep(random_time)
        aviaoAgent.start()
        i += 1
        lista_agentes_avioes.append(aviaoAgent)


    # Handle interruption of all agents
    while torre_controlo.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # stop all customer Agents
            for aviao in lista_agentes_avioes:
                aviao.stop()

            # parar os restantes agentes
            torre_controlo.stop()
            gestor_de_gares.stop()
            dashboard.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()



if '__name__' == '__main__':
    main()