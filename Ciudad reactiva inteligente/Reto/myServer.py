import mesa  # type: ignore
import json
from dataclasses import dataclass
from Model_Reto import Model, Car, People, Bus, Semaforo # type: ignore
from flask import Flask, redirect, url_for, request  # type: ignore
app = Flask(__name__)


@dataclass
class TrafficLight:
    id: int
    estado: str
    grupo: int
    type: str

@dataclass
class Lista_semaforos:
    semaforos: list[TrafficLight]

@dataclass
class Agent:
    x: int
    y: int
    id: int
    direccion: int
    type: str

@dataclass
class Agent_List:
    agents: list[Agent]


model = Model(100) # Variable global para el modelo (100 es el numero de agentes)


# Rutas para actualizar a los agentes
@app.route('/people_positions', methods = ['GET'])
def people_positions():
    agents = model.schedule.agents
    people = [obj for obj in agents if isinstance(obj, People)]
    return json.dumps(Agent_List([Agent(person.pos[0], person.pos[1], person.unique_id, person.direction, "per",).__dict__ for person in people]).__dict__)

@app.route('/cars_positions', methods = ['GET'])
def cars_positions():
    agents = model.schedule.agents
    cars = [obj for obj in agents if isinstance(obj, Car)]
    return json.dumps(Agent_List([Agent(car.pos[0], car.pos[1], car.unique_id, car.direction, "car").__dict__ for car in cars]).__dict__)

@app.route('/buses_positions', methods = ['GET'])
def buses_positions():
    agents = model.schedule.agents
    buses = [obj for obj in agents if isinstance(obj, Bus)]
    return json.dumps(Agent_List([Agent(bus.pos[0], bus.pos[1], bus.unique_id, bus.direction, "bus").__dict__ for bus in buses]).__dict__)

@app.route('/traffic_lights', methods = ['GET'])
def semaforos_positions():
    agents = model.schedule.agents
    semaforos = [obj for obj in agents if isinstance(obj, Semaforo)]
    return json.dumps(Lista_semaforos([TrafficLight(semaforo.unique_id, semaforo.estado, semaforo.group, "sem").__dict__ for semaforo in semaforos]).__dict__)

  
# La ruta para ejecutar un solo step del modelo
@app.route('/stps', methods = ['GET'])
def stps():
    model.step()
    return "OK"

if __name__ == '__main__':
    app.run(debug = True)