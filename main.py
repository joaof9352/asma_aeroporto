from spade import agent, quit_spade

from Agents.AviaoAgent import AviaoAgent
from Agents.GestorDeGaresAgent import GestorDeGaresAgent
from Agents.TorreDeControloAgent import TorreDeControloAgent
from Agents.DashboardAgent import DashboardAgent
import random
import time

XMPP_SERVER = 'legion'
PASSWORD = 'openfireASMA'

MAX_AVIOES = 5  # limit number of taxis



def main():
    i = 0

    # Initialize list to save all active Agents in list
    lista_agentes_avioes = []

    torre_controlo_jid = "torre@" + XMPP_SERVER
    gestor_de_gares_jid = "gestor_de_gares@" + XMPP_SERVER
    dashboard_jid = "dashboard@" + XMPP_SERVER

    torre_controlo = TorreDeControloAgent(torre_controlo_jid, PASSWORD)
    gestor_de_gares = GestorDeGaresAgent(gestor_de_gares_jid, PASSWORD)
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)

    # Fazer set dos agentes para que possam comunicar entre si

    torre_controlo.set('Gestor De Gares', gestor_de_gares_jid)
    torre_controlo.set('Dashboard', dashboard_jid)

    gestor_de_gares.set('Torre De Controlo', torre_controlo_jid)
    gestor_de_gares.set('Dashboard', dashboard_jid)

    dashboard.set('Torre De Controlo', torre_controlo_jid)
    dashboard.set('Gestor De Gares', gestor_de_gares_jid)

    # Inicializar os agentes principais (torre de controlo, gestor de gares e dashboard)

    res_gest = gestor_de_gares.start(auto_register=True)
    res_gest.result()
    time.sleep(1)
    res_dashboard = dashboard.start(auto_register=True)
    res_dashboard.result()
    time.sleep(1)
    res_torre = torre_controlo.start(auto_register=True)
    res_torre.result()
    time.sleep(1)

    while i < MAX_AVIOES:
        random_time = random.randint(1, 10)
        aviaoAgent = AviaoAgent(f"plane{i}@"+XMPP_SERVER, PASSWORD)
        aviaoAgent.set('Torre De Controlo', torre_controlo_jid) # Fazer com que o avião conheça a torre de controlo, para que possa comunicar com ela
        res_aviao = aviaoAgent.start(auto_register=True)
        res_aviao.result()
        #dashboard.set('Gestor De Gares', gestor_de_gares_jid)
        time.sleep(random_time)
        i += 1
        lista_agentes_avioes.append(aviaoAgent)


    # Handle interruption of all agents
    while torre_controlo.is_alive():
        #print("Agents running...")
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



if __name__ == '__main__':
    main()