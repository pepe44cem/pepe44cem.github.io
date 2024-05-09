# Visualizar el modelo de simulación
# Autores: José Antonio Moreno Tahuilan A01747922
#          Ángel Armando Márquez Curiel A01750147
#          Hector Gonzalez Sanchez A01753863
#          Alfredo Azamar López A01798100
# Fecha de creación/modificación: 16 11 2023

import mesa # type: ignore
import random
import numpy as np
from mesa.experimental import JupyterViz # type: ignore
import solara
from matplotlib.figure import Figure
import time

from typing import Tuple, Iterator, Dict, List
from collections import deque

from Model_Reto import Model
from Agentes_Reto import *

def agent_portrayal(agent):
        if isinstance(agent, Car):
            return {"color": "tab:orange","size": 50, "layer": 1}
        elif isinstance(agent, Bus):
            return {"color": "tab:purple","size": 50, "layer": 1}
        elif isinstance(agent, Parking_In):
            return {"color": "yellow","size": 50, "layer": 1}
        elif isinstance(agent, Parking_Out):
            return {"color": "yellow","size": 50, "layer": 1}
        elif isinstance(agent, Corner):
            return {"color": "brown", "size": 50, "layer": 10}
        elif isinstance(agent, Builing):
            return {"color": "tab:blue", "size": 50, "layer": 1}
        elif isinstance(agent, Semaforo):
            if agent.estado == 'rojo':
                return {"color": "red","size": 50, "layer": 1}
            else:
                return {"color": "green","size": 50, "layer": 1}
        elif isinstance(agent, SideWalk):
            return {"color": "grey","size": 50, "layer": 1}
        elif isinstance(agent, People):
            return {"color": "black", "size": 50, "layer": 1}


model_params = {
    "num_agents": {
        "value": 1
    }
}

page = JupyterViz(
    Model,
    model_params,
    measures=[],
    name="Cleaning Environment",
    agent_portrayal=agent_portrayal
    
)
# This is required to render the visualization in the Jupyter notebook
page