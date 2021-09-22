import math
import json
from typing import NamedTuple
import pandas as pd

class Node(NamedTuple):
  origins: str
  destination: str
  distance: int
  duration: int
  cost: int

dataCost = pd.read_excel("DataAirportlink.xlsx", sheet_name='price').to_dict()
dataTime = pd.read_excel("DataAirportlink.xlsx", sheet_name='time').to_dict()

stations: list[str] = []
for index in dataCost['Unnamed: 0']:
  stations.append(dataCost['Unnamed: 0'][index])

print(dataCost)

nodes: list[Node] = []
for index in range(len(stations)):
  origins = stations[index]
  # print('origins '+origins)
  destinatiosCost = dataCost[origins]
  for destinationIndex in destinatiosCost:
    destination = stations[destinationIndex]
    if (origins == destination): continue
    time = dataTime[origins][destinationIndex] * 60
    cost = destinatiosCost[destinationIndex]
    if math.isnan(time):
      time = 0
    if math.isnan(cost):
      cost = 0
    node = Node(origins, destination, 0, time, destinatiosCost[destinationIndex])
    nodes.append(node)


jsonNodes: list[str] = []
for node in nodes:
  jsonNodes.append(node._asdict())

with open('nodes-apr.json', 'w', encoding='utf8') as outfile:
  json.dump(jsonNodes, outfile, indent=2, ensure_ascii=False)
