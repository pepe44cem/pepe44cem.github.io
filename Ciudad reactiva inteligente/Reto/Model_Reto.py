# Modelo de la simulación
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

from Agentes_Reto import *


# --------------------------------------- Constantes ---------------------------------------
# Ruta de los buses -------->
# Ruta A:
PATH_BUSES_RA = [(13, 45, 3), (2, 45, 2), (2, 38, 2), (2, 2, 4), 
              (5, 2, 4), (45, 2, 1), (45, 5, 1), (45, 42, 1), 
              (45, 45, 3), (14, 45, 3)]

BUS_STOP_A = {(13, 45), (2, 38), (5, 2), (45, 5), (45, 42)}


# Ruta B:
PATH_BUSES_RB = [(22, 46, 3), (1, 46, 2), (1, 27, 2), (1, 13, 2),
                 (1, 1, 4), (38, 1, 4), (46, 1, 1), (46, 26, 1),
                 (46, 46, 3), (23, 46, 3)]

BUS_STOP_B = {(22, 46), (1, 27), (1, 13), (38, 1), (46, 26)}

# Ruta C:
PATH_BUSES_RC = [(25, 29, 2), (25, 10, 2), (25, 1, 4), (30, 1, 1),
                 (30, 14, 1), (30, 30, 1), (30, 39, 1), (30, 46, 3),
                 (25, 46, 2), (25, 30, 2)]

BUS_STOP_C = {(25, 29), (25, 10), (30, 14), (30, 30), (30, 39)}

# Ruta D:
PATH_BUSES_RD = [(22, 22, 3), (15, 22, 3), (1, 22, 2), (1, 17, 4),
                 (7, 17, 4), (37, 17, 4), (46, 17, 1), (46, 22, 3),
                 (34, 22, 3), (23, 22, 3)]

BUS_STOP_D = {(22, 22), (15, 22), (7, 17), (37, 17), (34, 22)}

# --------------------------------------- Clase Modelo ---------------------------------------
class Model(mesa.Model):
    
    def get_agent_by_id(self, agent_id):
        for agent in self.schedule.agents:
            if agent.unique_id == agent_id:
                return agent
        return None
    
    def __init__(self, num_agents):
        """A cleaning environment model which contains cleaning robots and dirty cells."""
        self.num_agents = num_agents
        self.grid = mesa.space.MultiGrid(48, 48, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.semaforos = set()
        self.corners = set()
        self.parqueosInicio = list()
        self.parqueosSalida = list()

        self.metroEntrances = list()
        self.metroExits = list()

        self.running = True
        self.cont = 0
        self.id= 0

        # ---------------------------- Borde Exterior ---------------------------------------
        # Banqueta -------->
        for x in range(0, 48):
            for y in range(0, 48):
                if y == 0 or y == 47 or x == 0 or x == 47:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (x, y))
                    # self.parqueos.append(a)
                    self.id+= 1

        # Corners -------->
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (0, 0))
        self.corners.add((0, 0))
        self.id += 1
        
        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (47, 0))
        self.corners.add((47, 0))
        self.id += 1
        
        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (47, 47))
        self.corners.add((47, 47))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (0, 47))
        self.corners.add((0, 47))
        self.id += 1
        
        # --------------------------------------- Bloque 1 ---------------------------------------
        # Edificios y Banquetas -------->
        for row in range(3, 13):
            for column in range(3, 17):
                if row == 3 or row == 12 or column == 3 or column == 16:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                    
                
        for row in range(15, 25):
            for column in range(3, 17):
                if row == 15 or row == 24 or column == 3 or column == 16:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        # Corners -------->
        # Edificio 1
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 3))
        self.corners.add((3, 3))
        self.id += 1

        a = Corner(self.id, self, [1, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (12, 3))
        self.corners.add((12, 3))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (12, 16))
        self.corners.add((12, 16))
        self.id += 1

        # SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (7, 16))
        self.corners.add((7, 16))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 16))
        self.corners.add((3, 16))
        self.id += 1

        # Edificio 2
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (15, 3))
        self.corners.add((15, 3))
        self.id += 1

        a = Corner(self.id, self, [1, 2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 3))
        self.corners.add((24, 3))
        self.id += 1

        # SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 10))
        self.corners.add((24, 10))
        self.id += 1

        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 0))
        self.corners.add((24, 0))
        self.id += 1

        a = Corner(self.id, self, [3, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 16))
        self.corners.add((24, 16))
        self.id += 1

        a = Corner(self.id, self, [2, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (15, 16))
        self.corners.add((15, 16))
        self.id += 1

        # --------------------------------------- Bloque 2 ---------------------------------------
        # Edificios y Banquetas -------->
        for row in range(31, 45):
            for column in range(3, 9):
                if row == 31 or row == 44 or column == 3 or column == 8:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        for row in range(31, 45):
            for column in range(11, 17):
                if row == 31 or row == 44 or column == 11 or column == 16:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        # Corners -------->
        #Edificio 1 (abajo)
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 3))
        self.corners.add((31, 3))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 3))
        self.corners.add((44, 3))
        self.id += 1

        a = Corner(self.id, self, [1, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 8))
        self.corners.add((44, 8))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 8))
        self.corners.add((31, 8))
        self.id += 1

        #Edificio 2 (arriba)
        a = Corner(self.id, self, [2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 11))
        self.corners.add((31, 11))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 11))
        self.corners.add((44, 11))
        self.id += 1

        a = Corner(self.id, self, [1, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 16))
        self.corners.add((44, 16))
        self.id += 1

        # SPECIAL CASE: METRO EXIT
        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 19))
        self.corners.add((44, 19))
        self.id += 1

        # SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (37, 16))
        self.corners.add((37, 16))
        self.id += 1

        a = Corner(self.id, self, [1, 2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 16))
        self.corners.add((31, 16))
        self.id += 1

        # SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 14))
        self.corners.add((31, 14))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (47, 16))
        self.corners.add((47, 16))
        self.id += 1

        


        # --------------------------------------- Bloque 3 ---------------------------------------
        # Edificios y Banquetas -------->
        for row in range(31, 37):
            for column in range(35, 45):
                if row == 31 or row == 36 or column == 35 or column == 44:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        for row in range(39, 45):
            for column in range(35, 45):
                if row == 39 or row == 44 or column == 35 or column == 44:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                    
        for row in range(31, 37):
            for column in range(23, 33):
                if row == 31 or row == 36 or column == 23 or column == 32:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        for row in range(39, 45):
            for column in range(23, 33):
                if row == 39 or row == 44 or column == 23 or column == 32:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        # Corners -------->
        # Edificio 1 (abajo izquierda)
        a = Corner(self.id, self, [3, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 23))
        self.corners.add((31, 23))
        self.id += 1

        # SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (34, 23))
        self.corners.add((34, 23))
        self.id += 1

        a = Corner(self.id, self, [1, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (36, 23))
        self.corners.add((36, 23))
        self.id += 1

        a = Corner(self.id, self, [1, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (36, 32))
        self.corners.add((36, 32))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 32))
        self.corners.add((31, 32))
        self.id += 1

        #SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 30))
        self.corners.add((31, 30))
        self.id += 1

        # Edificio 2 (abajo derecha)
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 23))
        self.corners.add((39, 23))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 23))
        self.corners.add((44, 23))
        self.id += 1

        a = Corner(self.id, self, [1, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 32))
        self.corners.add((44, 32))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 32))
        self.corners.add((39, 32))
        self.id += 1

        # Edificio 3 (arriba izquierda)
        a = Corner(self.id, self, [2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 35))
        self.corners.add((31, 35))
        self.id += 1

        a = Corner(self.id, self, [1, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (36, 35))
        self.corners.add((36, 35))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (36, 44))
        self.corners.add((36, 44))
        self.id += 1

        a = Corner(self.id, self, [1, 2, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 44))
        self.corners.add((31, 44))
        self.id += 1

        #SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 39))
        self.corners.add((31, 39))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 47))
        self.corners.add((31, 47))
        self.id += 1

        # Edificio 4 (arriba derecha)
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 35))
        self.corners.add((39, 35))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 35))
        self.corners.add((44, 35))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 44))
        self.corners.add((44, 44))
        self.id += 1

        a = Corner(self.id, self, [2, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 44))
        self.corners.add((39, 44))
        self.id += 1

        # --------------------------------------- Bloque 4 ---------------------------------------
        # Edificios y Banquetas -------->
        for row in range(3, 25):
            for column in range(35, 45):
                if row == 3 or row == 24 or column == 35 or column == 44:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
        
        for row in range(3, 11):
            for column in range(23, 33):
                if row == 3 or row == 10 or column == 23 or column == 32:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
        
        for row in range(13, 25):
            for column in range(23, 33):
                if row == 13 or row == 24 or column == 23 or column == 32:
                    a = SideWalk(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1
                else:
                    a = Builing(self.id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (row, column))
                    self.id+= 1

        # Corners -------->
        # Edificio 1 (abajo izquierda)
        a = Corner(self.id, self, [2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 23))
        self.corners.add((3, 23))
        self.id += 1

        a = Corner(self.id, self, [1, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (10, 23))
        self.corners.add((10, 23))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (10, 32))
        self.corners.add((10, 32))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 32))
        self.corners.add((3, 32))
        self.id += 1

        # Corners -------->
        # Edificio 2 (abajo derecha)
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 23))
        self.corners.add((13, 23))
        self.id += 1

        #SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (22, 23))
        self.corners.add((22, 23))
        self.id += 1

        #SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (15, 23))
        self.corners.add((15, 23))
        self.id += 1

        a = Corner(self.id, self, [1, 2])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 23))
        self.corners.add((24, 23))
        self.id += 1

        #SPECIAL CASE: BUS STOP
        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 29))
        self.corners.add((24, 29))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 32))
        self.corners.add((24, 32))
        self.id += 1

        a = Corner(self.id, self, [1, 2, 3])
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 32))
        self.corners.add((13, 32))
        self.id += 1

        # Corners -------->
        # Edificio 3 (arriba)
        a = Corner(self.id, self, [2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 35))
        self.corners.add((3, 35))
        self.id += 1

        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 35))
        self.corners.add((13, 35))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 35))
        self.corners.add((24, 35))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 44))
        self.corners.add((24, 44))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 44))
        self.corners.add((3, 44))
        self.id += 1

        a = Corner(self.id, self, [2, 4])
        self.schedule.add(a)
        self.grid.place_agent(a, (0, 23))
        self.corners.add((0, 23))
        self.id += 1

        # --------------------------------------- Corners (left-out) ---------------------------------------

        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (28, 3))
        self.corners.add((28, 3))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 20))
        self.corners.add((44, 20))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (27, 44))
        self.corners.add((27, 44))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 19))
        self.corners.add((3, 19))
        self.id += 1

        a = Corner(self.id, self, [4])
        self.schedule.add(a)
        self.grid.place_agent(a, (28, 16))
        self.corners.add((28, 16))
        self.id += 1

        a = Corner(self.id, self, [1])
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 20))
        self.corners.add((31, 20))
        self.id += 1

        a = Corner(self.id, self, [3])
        self.schedule.add(a)
        self.grid.place_agent(a, (27, 23))
        self.corners.add((27, 23))
        self.id += 1

        a = Corner(self.id, self, [2])
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 19))
        self.corners.add((24, 19))
        self.id += 1

        # --------------------------------------- Camellones ---------------------------------------
        # Glorieta -------->
        for row in range(26, 30):
            for column in range(18, 22):
                a = Builing(self.id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (row, column))
                self.id+= 1
        
        # Verticales -------->
        for row in range(27, 29):
            for column in range(23, 45):
                a = Builing(self.id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (row, column))
                self.id+= 1

        for row in range(27, 29):
            for column in range(3, 17):
                a = Builing(self.id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (row, column))
                self.id+= 1

        # Horizontales -------->
        for row in range(3, 25):
            for column in range(19, 21):
                a = Builing(self.id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (row, column))
                self.id+= 1

        for row in range(31, 45):
            for column in range(19, 21):
                a = Builing(self.id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (row, column))
                self.id+= 1
        
        
        # ------------------------------------- Estacionamientos ------------------------------------
        # Número (1):
        # --- IN ---
        a = Parking_In(self.id, self, 1, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (19, 43))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 1, 2, 0)
        self.schedule.add(a)
        self.grid.place_agent(a, (18, 43))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (2):
        # --- IN ---
        a = Parking_In(self.id, self, 3, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (4, 41))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 3, 4, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (4, 40))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (3):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (35, 41))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 4, 3, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (35, 40))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (4):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (23, 39))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 4, 3, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (23, 38))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (5):
        # --- IN ---
        a = Parking_In(self.id, self, 3, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (40, 39))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 3, 4, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (40, 38))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (6):
        # --- IN ---
        a = Parking_In(self.id, self, 2, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (12, 36))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 2, 1, 5)
        self.schedule.add(a)
        self.grid.place_agent(a, (11, 36))
        self.parqueosSalida.append(a)
        self.id+= 1

        # Número (7):
        # --- IN ---
        a = Parking_In(self.id, self, 1, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (17, 31))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        a = Parking_Out(self.id, self, 1, 2, 6)
        self.schedule.add(a)
        self.grid.place_agent(a, (16, 31))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (8):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (43, 28))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        a = Parking_Out(self.id, self, 4, 3, 7)
        self.schedule.add(a)
        self.grid.place_agent(a, (43, 29))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (9):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (9, 26))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 4, 3, 8)
        self.schedule.add(a)
        self.grid.place_agent(a, (9, 27))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (10):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (23, 27))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 4, 3, 9)
        self.schedule.add(a)
        self.grid.place_agent(a, (23, 26))
        self.parqueosSalida.append(a)
        self.id+= 1

        # Número (11):
        # --- IN ---
        a = Parking_In(self.id, self, 3, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (32, 26))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 3, 4, 10)
        self.schedule.add(a)
        self.grid.place_agent(a, (32, 27))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (12):
        # --- IN ---
        a = Parking_In(self.id, self, 3, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (4, 13))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 3, 4, 11)
        self.schedule.add(a)
        self.grid.place_agent(a, (4, 12))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (13):
        # --- IN ---
        a = Parking_In(self.id, self, 2, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (35, 12))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 2, 1, 12)
        self.schedule.add(a)
        self.grid.place_agent(a, (34, 12))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (14):
        # --- IN ---
        a = Parking_In(self.id, self, 2, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 12))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 2, 1, 13)
        self.schedule.add(a)
        self.grid.place_agent(a, (38, 12))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (15):
        # --- IN ---
        a = Parking_In(self.id, self, 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (11, 7))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 4, 3, 14)
        self.schedule.add(a)
        self.grid.place_agent(a, (11, 6))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (16):
        # --- IN ---
        a = Parking_In(self.id, self, 3, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (16, 7))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 3, 4, 15)
        self.schedule.add(a)
        self.grid.place_agent(a, (16, 6))
        self.parqueosSalida.append(a)
        self.id+= 1


        # Número (17):
        # --- IN ---
        a = Parking_In(self.id, self, 1, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (39, 7))
        self.parqueosInicio.append(a)
        self.id+= 1

        # --- OUT ---
        # __Pensando que el parametro de numero es el numero de estacionamiento al que se dirige__
        a = Parking_Out(self.id, self, 1, 2, 16)
        self.schedule.add(a)
        self.grid.place_agent(a, (38, 7))
        self.parqueosSalida.append(a)
        self.id+= 1 

        # ---------------------------------------- Semáforos ----------------------------------------
        # Grupo 1 -------->
        a = Semaforo(self.id, self, 'verde', 1, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 2))
        self.semaforos.add((24, 2))
        self.id+= 1
        
        a = Semaforo(self.id, self, 'verde', 1, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (24, 1))
        self.semaforos.add((24, 1))
        self.id+= 1

        # Grupo 2 -------->
        a = Semaforo(self.id, self, 'rojo', 2, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (26, 3))
        self.semaforos.add((26, 3))
        self.id+= 1

        a = Semaforo(self.id, self, 'rojo', 2, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (25, 3))
        self.semaforos.add((25, 3))
        self.id+= 1

        # Grupo 3 -------->
        a = Semaforo(self.id, self, 'rojo', 3, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (45, 16))
        self.semaforos.add((45, 16))
        self.id+= 1

        a = Semaforo(self.id, self, 'rojo', 3, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (46, 16))
        self.semaforos.add((46, 16))
        self.id+= 1

        # Grupo 4 -------->
        a = Semaforo(self.id, self, 'verde', 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 18))
        self.semaforos.add((44, 18))
        self.id+= 1
        
        a = Semaforo(self.id, self, 'verde', 4, 3)
        self.schedule.add(a)
        self.grid.place_agent(a, (44, 17))
        self.semaforos.add((44, 17))
        self.id+= 1

        # Grupo 5 -------->        
        a = Semaforo(self.id, self, 'verde', 5, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 46))
        self.semaforos.add((31, 46))
        self.id+= 1

        a = Semaforo(self.id, self, 'verde', 5, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 45))
        self.semaforos.add((31, 45))
        self.id+= 1

        # Grupo 6 -------->
        a = Semaforo(self.id, self, 'rojo', 6, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (29, 44))
        self.semaforos.add((29, 44))
        self.id+= 1

        a = Semaforo(self.id, self, 'rojo', 6, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (30, 44))
        self.semaforos.add((30, 44))
        self.id+= 1

        # Grupo 7 -------->
        a = Semaforo(self.id, self, 'rojo', 7, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (1, 23))
        self.semaforos.add((1, 23))
        self.id+= 1
        
        a = Semaforo(self.id, self, 'rojo', 7, 1)
        self.schedule.add(a)
        self.grid.place_agent(a, (2, 23))
        self.semaforos.add((2, 23))
        self.id+= 1

        # Grupo 8 -------->
        a = Semaforo(self.id, self, 'verde', 8, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 22))
        self.semaforos.add((3, 22))
        self.id+= 1

        a = Semaforo(self.id, self, 'verde', 8, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (3, 21))
        self.semaforos.add((3, 21))
        self.id+= 1

        # Grupo 9 -------->
        a = Semaforo(self.id, self, 'rojo', 9, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (29, 8))
        self.semaforos.add((29, 8))
        self.id+= 1

        a = Semaforo(self.id, self, 'rojo', 9, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (30, 8))
        self.semaforos.add((30, 8))
        self.id+= 1

        # Grupo 10 -------->
        a = Semaforo(self.id, self, 'verde', 10, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 10))
        self.semaforos.add((31, 10))
        self.id+= 1

        a = Semaforo(self.id, self, 'verde', 10, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (31, 9))
        self.semaforos.add((31, 9))
        self.id+= 1
    
        # Grupo 11 -------->
        a = Semaforo(self.id, self, 'rojo', 11, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (11, 32))
        self.semaforos.add((11, 32))
        self.id+= 1
        
        a = Semaforo(self.id, self, 'rojo', 11, 2)
        self.schedule.add(a)
        self.grid.place_agent(a, (12, 32))
        self.semaforos.add((12, 32))
        self.id+= 1

        # Grupo 12 -------->
        a = Semaforo(self.id, self, 'verde', 12, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 34))
        self.semaforos.add((13, 34))
        self.id+= 1

        a = Semaforo(self.id, self, 'verde', 12, 4)
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 33))
        self.semaforos.add((13, 33))
        self.id+= 1

        # --------------------------------------- Autobuses ---------------------------------------
        # Ejemplo 1
        a = Bus(self.id, self, PATH_BUSES_RA, BUS_STOP_A)
        self.schedule.add(a)
        self.grid.place_agent(a, (13, 45))
        self.id += 1

        # Ejemplo 2
        a = Bus(self.id, self, PATH_BUSES_RB, BUS_STOP_B)
        self.schedule.add(a)
        self.grid.place_agent(a, (22, 46))
        self.id += 1

        # Ejemplo 3
        a = Bus(self.id, self, PATH_BUSES_RC, BUS_STOP_C)
        self.schedule.add(a)
        self.grid.place_agent(a, (25, 29))
        self.id += 1

        # Ejemplo 4
        a = Bus(self.id, self, PATH_BUSES_RD, BUS_STOP_D)
        self.schedule.add(a)
        self.grid.place_agent(a, (22, 22))
        self.id += 1    

       
    def step(self):
            self.schedule.step()
            if (self.cont <= 50):
                a = People(self.id, self, 3)
                self.schedule.add(a)
                self.grid.place_agent(a, (21, 16))
                self.id += 1
                self.cont += 1

                a = People(self.id, self, 4)
                self.schedule.add(a)
                self.grid.place_agent(a, (18, 23))
                self.id += 1
                self.cont += 1