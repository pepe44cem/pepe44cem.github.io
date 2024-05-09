# Desarrollo de los Agentes para el modelado.
# Autores: José Antonio Moreno Tahuilan A01747922
#          Ángel Armando Márquez Curiel A01750147
#          Héctor Gonzalez Sanchez A01753863
#          Alfredo Azamar López A01798100
# Fecha de creación/modificación: 16 11 2023

import mesa # type: ignore
import random
import numpy as np
from mesa.experimental import JupyterViz # type: ignore
import solara
from matplotlib.figure import Figure
import time

from grafo import *


# Graph = dict[tuple[int, int], set[tuple[int, int, int, int]]]
# EXAMPLE --- > (x, y): {(x, y, direction, weight)}

# --------------------------------------- Constantes ---------------------------------------

PASSENGER_STOP = {(13, 44), (3, 38), (5, 3), (44, 5), (44, 42),
                  (22, 47), (0, 27), (0, 13), (38, 0), (47, 26),
                  (24, 29), (24, 10), (31, 14), (31, 30), (31, 39),
                  (22, 23), (15, 23), (7, 16), (37, 16), (34, 23)}

WAITING_TIME = 40
TIEMPO_CAMBIO = 40
CAPACIDAD_ESTACIONAMIENTO = 45
AUTOS_PRINCIPIO = 10
CAPACITY_METRO = 100
PEOPLE_METRO = 15
CAPACITY_BUSES = 5
TIEMPO_SPAWN = 30
UMBRAL_SPANW = 80
UMBRAL_DECISION_E = 50
UMBRAL_DECISION_S = 20
DENSITY_PEOPLE = 5
MAX_DESPERATION_TIME = 3


class Semaforo(mesa.Agent):
    """The agent traffic light in our city."""

    def __init__(self, unique_id, model, estado, group, dir):
        super().__init__(unique_id, model)
        self.steps = 0
        self.estado = estado
        self.group = group
        self.dir = dir
        #self.weight = 0
        self.priority = False
        self.groupWeight = 0
        self.otherGroup = self.group + 1 if self.group % 2 != 0 else self.group - 1
        # self.otherGroup = self.group + 1 if self.group % 2 != 0 else self.group - 1
        self.otherGroupWeight = 0
        
        # CHECAR DEFINCIONES DE SEMÁFOROS

        # Filtar por tipo de agente (Carro y Bus)
        # Hacemos un len de la lista filtrada
        # Acceder al peso del vecino semáforo y lo actualizamos (ID: Mediante impar / par)
        # Comparar el peso del grupo vecino con el peso del semáforo actual y dar paso (Mediante impar / par)

        """
        REGLAS DE PASAR: (CAMBIAR ESTADO)
        MAYOR --> PASO
        MENOR --> ESPERO
        IGUAL -- > PAR
        """
    def checkTraffic(self):
        x, y = self.pos
        if (self.dir == 1):
            myCells = [(x, y + i) for i in range(1, 6)]
            cellContent = self.model.grid.get_cell_list_contents(myCells)
            traffic = [obj for obj in cellContent if isinstance(obj, Car) or isinstance(obj, Bus)]
            # print(f'POS: {self.pos} -- MINE: {myCells} -- GROUP: {self.group}')
        elif (self.dir == 2):
            myCells = [(x, y - i) for i in range(1, 6)]
            cellContent = self.model.grid.get_cell_list_contents(myCells)
            traffic = [obj for obj in cellContent if isinstance(obj, Car) or isinstance(obj, Bus)]
            # print(f'POS: {self.pos} -- MINE: {myCells} -- GROUP: {self.group}')
        elif (self.dir == 3):
            myCells = [(x - i, y) for i in range(1, 6)]
            cellContent = self.model.grid.get_cell_list_contents(myCells)
            traffic = [obj for obj in cellContent if isinstance(obj, Car) or isinstance(obj, Bus)]
            # print(f'POS: {self.pos} -- MINE: {myCells} -- GROUP: {self.group}')
        elif (self.dir == 4):
            myCells = [(x + i, y) for i in range(1, 6)]
            cellContent = self.model.grid.get_cell_list_contents(myCells)
            traffic = [obj for obj in cellContent if isinstance(obj, Car) or isinstance(obj, Bus)]
            # print(f'POS: {self.pos} -- MINE: {myCells} -- GROUP: {self.group}')
        return len(traffic)


    def cambioEstado(self):
        if self.estado == 'rojo':
            self.estado = 'verde'
        else:
            self.estado = 'rojo'
        # allTFL = [agent for agent in self.model.schedule.agents if isinstance(agent, Semaforo)]
        
        # # Filtrarlos por grupo
        # if self.group % 2 != 0:
        #     otherGroup = self.group + 1
        # else:
        #     otherGroup = self.group - 1

        # if (newStatus):
        #     self.estado = newStatus
        #     self.priority = False
        # else:
        #     if (self.priority):
        #         if self.estado == 'rojo':
        #             self.estado = 'verde'
        #         else:
        #             self.estado = 'rojo'
        #         self.steps = 0
        #         self.priority = False
        #         for trafficLight in allTFL:
        #             if trafficLight.group == otherGroup:
        #                 trafficLight.cambioEstado('rojo')

    def step(self):
        self.steps += 1
        #self.weight = self.checkTraffic() # Peso del semáforo actual
        self_group_agent = [agent for agent in self.model.schedule.agents if isinstance(agent, Semaforo) and agent.group == self.group]
        other_group_agent = [agent for agent in self.model.schedule.agents if isinstance(agent, Semaforo) and agent.group == self.otherGroup]
        self.groupWeight = sum(trafficLight.checkTraffic() for trafficLight in self_group_agent)
        self.otherGroupWeight = sum(trafficLight.checkTraffic() for trafficLight in other_group_agent)
        
        posTL = [agent.pos for agent in self_group_agent]
        posTLC = [agent.pos for agent in other_group_agent]

        peopleIn = [agent for agent in self.model.schedule.agents if isinstance(agent, People) and agent.pos in posTL]
        peopleInC = [agent for agent in self.model.schedule.agents if isinstance(agent, People) and agent.pos in posTLC]
        #allTFL = [agent for agent in self.model.schedule.agents if isinstance(agent, Semaforo)]

        # Filtrarlos por grupo
        # if self.group % 2 != 0:
        #     otherGroup = self.group + 1
        # else:
        #     otherGroup = self.group - 1

        #moreTFL = [trafficLight for trafficLight in allTFL if trafficLight.group == otherGroup]
        #totalWeight = sum(trafficLight.weight for trafficLight in moreTFL)
        # print(f'SELF WEIGHT: {self.groupWeight} -- TOTAL WEIGHT: {self.otherGroupWeight} -- GROUP: {self.group} -- OTHER GROUP: {self.otherGroup}')
            
        if len(peopleIn) == 0 and len(peopleInC) == 0:

        # Comparacion de pesos
            if (self.groupWeight > self.otherGroupWeight):
                for trafficLight in self_group_agent:
                    trafficLight.estado = 'verde'
                for trafficLight in other_group_agent:
                    trafficLight.estado = 'rojo'
            elif (self.groupWeight > self.otherGroupWeight):
                for trafficLight in self_group_agent:
                    trafficLight.estado = 'rojo'
                for trafficLight in other_group_agent:
                    trafficLight.estado = 'verde'
            elif (self.groupWeight == self.otherGroupWeight):
                if self.group % 2 == 0:
                    for trafficLight in self_group_agent:
                        trafficLight.estado = 'verde'
                    for trafficLight in other_group_agent:
                        trafficLight.estado = 'rojo'
                else:
                    for trafficLight in self_group_agent:
                        trafficLight.estado = 'rojo'
                    for trafficLight in other_group_agent:
                        trafficLight.estado = 'verde'

        # elif (self.weight < totalWeight):
        #     # Cambiar el otro grupo a verde
        #     for trafficLight in allTFL:
        #         if trafficLight.group == otherGroup:
        #             trafficLight.priority = True
        # elif (self.weight == totalWeight):
        #     # Cambiar el otro grupo a par
        #     if self.group % 2 == 0:
        #         for trafficLight in allTFL:
        #             if trafficLight.group == self.group:
        #                 trafficLight.priority = True

        # sameGroupTFL = [trafficLight for trafficLight in allTFL if trafficLight.group == self.group]
        # if all(trafficLight.priority == sameGroupTFL[0].priority for trafficLight in sameGroupTFL):
        #     for trafficLight in sameGroupTFL:
        #         trafficLight.cambioEstado()

        # print(f'ID: {self.unique_id} -- POS: {self.pos} -- WEIGHT: {self.weight}')


class Car(mesa.Agent):
    """Representa un agente de un coche en tu modelo."""
    def __init__(self, unique_id, model, inicio, fin):
        super().__init__(unique_id, model)
        self.inicio = inicio
        self.fin = fin
        self.start = self.model.parqueosSalida[self.inicio].pos
        self.end = self.model.parqueosInicio[self.fin].pos
        self.overtakes = desviacionesSet
        self.path = breadth_first_search(self.start, self.end, graph)
        self.stepStop = 0
        self.desperationTime = MAX_DESPERATION_TIME
        
        direccionSalid = self.model.parqueosSalida[self.inicio].direccionSalida
        primerNodo = tuple(list(self.path[0]) + [direccionSalid])
        self.path = [primerNodo] + self.path[1:]
        self.direction = self.path[0][2]
        self.index = 0


    def futurePosition(self):
        x, y = self.pos
        if self.direction == 1:
            return (x, y + 1)
        elif self.direction == 2:
            return (x, y - 1)
        elif self.direction == 3:
            return (x - 1, y)
        elif self.direction == 4:
            return (x + 1, y)


    def futureOvertake(self):
        x, y = self.pos
        if self.direction == 1 and (x == 30 or x == 46):
            return (x - 1, y + 1)
        
        elif self.direction == 1:
            return (x + 1, y + 1)
        
        elif self.direction == 2 and (x == 25 or x == 37 or x == 1):
            return (x + 1, y - 1)
        
        elif self.direction == 3 and y == 45:
            return (x - 1, y + 1)
        
        elif self.direction == 3 and y == 22:
            return (x - 1, y - 1)
        
        elif self.direction == 2 or self.direction == 3:
            return (x - 1, y - 1)
        
        elif self.direction == 4 and (y == 1 or y == 17):
            return (x + 1, y + 1)

        elif self.direction == 4:
            return (x + 1, y - 1)
        

    def freeOvertake(self):
        x, y = self.pos
        if self.direction == 1 and (x == 30 or x == 46):
            cell = self.model.grid.get_cell_list_contents([x - 1, y + 1]) + self.model.grid.get_cell_list_contents([x - 1, y])
            if len(cell) == 0:
                return True
            
        elif self.direction == 1:
            cell = self.model.grid.get_cell_list_contents([x + 1, y + 1]) + self.model.grid.get_cell_list_contents([x + 1, y])
            if len(cell) == 0:
                return True
            
        elif self.direction == 2 and (x == 25 or x == 37 or x == 1):
            cell = self.model.grid.get_cell_list_contents([x + 1, y - 1]) + self.model.grid.get_cell_list_contents([x + 1, y])
            if len(cell) == 0:
                return True
            
        elif self.direction == 3 and y == 45:
            cell = self.model.grid.get_cell_list_contents([x - 1, y + 1]) + self.model.grid.get_cell_list_contents([x, y + 1])
            if len(cell) == 0:
                return True
            

        elif self.direction == 3 and y == 22:
            cell = self.model.grid.get_cell_list_contents([x - 1, y - 1]) + self.model.grid.get_cell_list_contents([x, y - 1])
            if len(cell) == 0:
                return True
        
        elif self.direction == 3:
            cell = self.model.grid.get_cell_list_contents([x - 1, y - 1]) + self.model.grid.get_cell_list_contents([x, y - 1])
            if len(cell) == 0:
                return True
            
        elif self.direction == 2:
            cell = self.model.grid.get_cell_list_contents([x - 1, y - 1]) + self.model.grid.get_cell_list_contents([x - 1, y])
            if len(cell) == 0:
                return True
        
        elif self.direction == 4 and (y == 1 or y == 17):
            cell = self.model.grid.get_cell_list_contents([x + 1, y + 1]) + self.model.grid.get_cell_list_contents([x, y + 1])
            if len(cell) == 0:
                return True
        
        elif self.direction == 4:
            cell = self.model.grid.get_cell_list_contents([x + 1, y - 1]) + self.model.grid.get_cell_list_contents([x, y - 1])
            if len(cell) == 0:
                return True
        return False


    def recalculatePath(self):
        self.path = breadth_first_search(self.pos, self.end, graph)
        # direccionSalid = self.model.parqueosSalida[self.inicio].direccionSalida
        # primerNodo = tuple(list(self.path[0]) + [direccionSalid])
        # self.path = [primerNodo] + self.path[1:]
        # self.direction = self.path[0][2]
        self.index = 0


    def step(self):
        # Checar si llegó al final del estacionamiento (es disponible),
        # si no es así, se calcula otra ruta
        if(self.pos == self.end):
            cell = self.model.grid.get_cell_list_contents([self.pos])
            parking = [obj for obj in cell if isinstance(obj, Parking_In)]
            if (parking[0].occupied < parking[0].capacity):
                parking[0].occupied += 1
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                return
            else:
                newPos = random.randint(0, 16)
                while newPos == self.fin:
                    newPos = random.randint(0, 16)

                posPepe = self.model.parqueosInicio[newPos].pos
                self.path = breadth_first_search(self.pos, posPepe, graph)
                
                direccionSalid = self.model.parqueosSalida[self.fin].direccionSalida

                primerNodo = tuple(list(self.path[0]) + [direccionSalid])
                
                self.path = [primerNodo] + self.path[1:] # Camino bueno
                self.direction = self.path[0][2] # Dirección del primer nodo
                self.index = 0 # Reiniciar el indice del camino
                self.fin = newPos # Cambiar el destino
                self.end = self.model.parqueosInicio[self.fin].pos

        if self.index < len(self.path) - 1:
            if self.pos == self.path[self.index][:2]:
                self.direction = self.path[self.index + 1][2]
                self.index += 1

        future = self.futurePosition()

        if self.model.grid.is_cell_empty(future):
            self.model.grid.move_agent(self, future)

        else:
            cell = self.model.grid.get_cell_list_contents([future])
            others = {obj for obj in cell if isinstance(obj, Car) or isinstance(obj, People) or isinstance(obj, Bus)}
            semaforo = [obj for obj in cell if isinstance(obj, Semaforo)]
            

            if future in self.model.semaforos:
                if semaforo[0].estado == "verde" and len(others) == 0:
                    self.model.grid.move_agent(self, future)
            elif len(others) == 0:
                self.model.grid.move_agent(self, future)
            else:
                if self.stepStop < self.desperationTime:
                    self.stepStop += 1
                elif (self.pos in self.overtakes and self.freeOvertake() and self.stepStop == self.desperationTime):
                    self.model.grid.move_agent(self, self.futureOvertake())
                    self.stepStop = 0
                    self.recalculatePath()
                elif self.pos in desviacionesGlorieta:
                    self.model.grid.move_agent(self, desviacionesGlorieta[self.pos])
                    self.stepStop = 0
                    self.direction = list(graph[self.pos])[0][2]
                    self.recalculatePath()


class Bus(mesa.Agent):
    """Representa un agente de un autobús en tu modelo."""
    def __init__(self, unique_id, model, path, stops):
        super().__init__(unique_id, model)
        self.path = path
        self.stops = stops
        self.cont = 0
        self.access = True
        self.capacity = CAPACITY_BUSES
        self.occupied = 0
        self.direction = self.path[0][2]
        self.index = 0

    def futurePosition(self):
        x, y = self.pos
        if self.direction == 1:
            return (x, y + 1)
        elif self.direction == 2:
            return (x, y - 1)
        elif self.direction == 3:
            return (x - 1, y)
        elif self.direction == 4:
            return (x + 1, y)
        
    def futureRide(self):
        x, y = self.pos

        if (x % 2 == 0):
            if (self.direction == 1 or self.direction == 2):
                return (x + 1, y)
        elif (x % 2 != 0):
            if (self.direction == 1 or self.direction == 2):
                return (x - 1, y)
            
        if (y % 2 == 0):
            if (self.direction == 3 or self.direction == 4):
                return (x, y + 1)
        elif (y % 2 != 0):
            if (self.direction == 3 or self.direction == 4):
                return (x, y - 1)
        # if self.direction == 1:
        #     return (x - 1, y)
        # elif self.direction == 2:
        #     return (x + 1, y)
        # elif self.direction == 3:
        #     return (x, y - 1)
        # elif self.direction == 4:
        #     return (x, y + 1)


    def step(self):

        # Final del camino
        if(self.pos == self.path[-1][:2]):
            self.index = 0
            self.direction = self.path[0][2]            

        # Movimiento
        if self.index < len(self.path) - 1:
            if self.pos == self.path[self.index + 1][:2]:
                self.direction = self.path[self.index + 1][2]
                self.index += 1

        future = self.futurePosition()

        if (self.pos in self.stops and self.cont == WAITING_TIME):
            self.access = not self.access
        
        # Esperar en la parada
        if (self.pos in self.stops and self.cont != WAITING_TIME):
            self.cont += 1
            num = random.randint(0, 100)
            if (not self.access and self.occupied > 0 and num < UMBRAL_DECISION_S):
                a = People(self.model.id, self.model, self.direction)
                self.model.schedule.add(a)
                self.model.grid.place_agent(a, self.futureRide())
                self.model.id += 1
                self.occupied -= 1

        elif (self.model.grid.is_cell_empty(future)):
            self.model.grid.move_agent(self, future)
            self.cont = 0

        else:
            cell = self.model.grid.get_cell_list_contents([future])
            others = {obj for obj in cell if isinstance(obj, Car) or isinstance(obj, People)}
            semaforo = [obj for obj in cell if isinstance(obj, Semaforo)]
            self.cont = 0

            if future in self.model.semaforos:
                if semaforo[0].estado == "verde" and len(others) == 0:
                    self.model.grid.move_agent(self, future)
            elif len(others) == 0:
                self.model.grid.move_agent(self, future)


class Parking_In(mesa.Agent):
    """
    """
    
    def __init__(self, unique_id, model, direccionSalida, direccionEntrada):
        super().__init__(unique_id, model)
        self.capacity = CAPACIDAD_ESTACIONAMIENTO
        self.occupied = AUTOS_PRINCIPIO
        self.direccionSalida = direccionSalida
        self.direccionEntrada = direccionEntrada
        self.tiempoSpawn = TIEMPO_SPAWN
    
    def step(self):
        ...
            
        
class Parking_Out(mesa.Agent):
    """
    """
    def __init__(self, unique_id, model, direccionSalida, direccionEntrada, numero):
        super().__init__(unique_id, model)
        self.numero = numero
        self.capacity = CAPACIDAD_ESTACIONAMIENTO
        self.occupied = AUTOS_PRINCIPIO
        self.direccionSalida = direccionSalida
        self.direccionEntrada = direccionEntrada
        self.tiempoSpawn = TIEMPO_SPAWN
        self.steps = TIEMPO_SPAWN - 1
        

    def step(self):
        self.occupied = self.model.get_agent_by_id(self.unique_id - 1).occupied
        self.steps += 1
        randomNumber = random.randint(0, 100)
        if randomNumber < UMBRAL_SPANW and self.steps % self.tiempoSpawn == 0 and self.occupied > 0:
            
            randomNumber = self.numero
            while randomNumber == self.numero:
                randomNumber = random.randint(0, 16)
            a = Car(self.model.id, self.model, self.numero, randomNumber)
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.model.parqueosSalida[self.numero].pos)
            self.model.id += 1 
            self.steps = 0
            self.occupied -= 1
            self.model.get_agent_by_id(self.unique_id - 1).occupied -= 1


class Builing(mesa.Agent):
    """
    """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        ...


class SideWalk(mesa.Agent):
    """
    """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        ...


class Corner(mesa.Agent):
    def __init__(self, unique_id, model, directions):
        super().__init__(unique_id, model)
        self.directions = directions

    def step(self):
        ...


class People(mesa.Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.direction = direction
        self.density = DENSITY_PEOPLE
    
    def move(self):
        lst = self.model.grid.get_cell_list_contents([self.futurePosition()])
        people = [obj for obj in lst if isinstance(obj, People)]
        if len(people) < self.density:
            self.model.grid.move_agent(self, self.futurePosition())

    def estoy_en_cruce(self):
        aux = (self.pos[0], self.pos[1], self.direction)
        if aux in crucePersonas:
            return True
        else:
            return False

    def estoy_en_corner(self):
        if self.pos in self.model.corners:
            return True
        else:
            return False

    def estoy_en_semaforo(self):
        if self.futurePosition() in self.model.semaforos:
            return True
        else:
            return False

    def freePass(self) -> bool:
        aux = (self.pos[0], self.pos[1], self.direction)
        lst = self.model.grid.get_cell_list_contents(crucePersonas[aux])
        result = [obj for obj in lst if isinstance(obj, People) or isinstance(obj, Car) or isinstance(obj, Bus)]
        return len(result) == 0
    

    def eleccion_es_cruce(self):
        aux = (self.pos[0], self.pos[1], self.direction)
        if aux in crucePersonas:
            return True
        else:
            return False

    def futurePosition(self):
        x, y = self.pos
        if self.direction == 1:
            return (x, y + 1)
        elif self.direction == 2:
            return (x, y - 1)
        elif self.direction == 3:
            return (x - 1, y)
        elif self.direction == 4:
            return (x + 1, y)
    
    def futureRide(self):
        x, y = self.pos
        if (x % 2 == 0):
            if (self.direction == 1 or self.direction == 2):
                return (x + 1, y)
        elif (x % 2 != 0):
            if (self.direction == 1 or self.direction == 2):
                return (x - 1, y)
            
        if (y % 2 == 0):
            if (self.direction == 3 or self.direction == 4):
                return (x, y + 1)
        elif (y % 2 != 0):
            if (self.direction == 3 or self.direction == 4):
                return (x, y - 1)
            
    def step(self):
        if self.estoy_en_corner():
            actual = self.model.grid.get_cell_list_contents([self.pos]) #CHECO LOS OBJETOS EN LA CORNER
            corner = [obj for obj in actual if isinstance(obj, Corner)] #OBTENGO LA CORNER DE MI POSICION
            self.direction = random.choice(corner[0].directions) #ELIGO UNA NUEVA DIRECCION ALEATORIA
            
            if self.eleccion_es_cruce():
                if self.freePass():
                    if self.estoy_en_semaforo():
                        future = self.futurePosition()
                        lst = self.model.grid.get_cell_list_contents([future])
                        semaforo = [obj for obj in lst if isinstance(obj, Semaforo)]
                        if semaforo[0].estado == "rojo":
                            self.move()
                    else:
                        self.move()
            else:
                self.move()
        else:
            self.move()

        if (self.pos in PASSENGER_STOP):
            myBus = self.futureRide()
            stopBus = self.model.grid.get_cell_list_contents([myBus])
            buses = [obj for obj in stopBus if isinstance(obj, Bus)]
            num = random.randint(0, 100)
            if (len(buses) > 0 and buses[0].access and buses[0].occupied < buses[0].capacity and num < UMBRAL_DECISION_E):
                self.model.grid.move_agent(self, myBus)
                buses[0].occupied += 1
                self.model.schedule.remove(self)
                self.model.grid.remove_agent(self)
                return
        # 1.- Si estoy en un cruce
        #     1.1.- Si estoy en semaforo
        #     1.2.- Si no estoy en semaforo
        # 2.- Si no estoy en un cruce
