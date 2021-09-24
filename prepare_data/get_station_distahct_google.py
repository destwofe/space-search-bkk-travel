import json
import requests
from typing import NamedTuple, Union
from concurrent.futures import ThreadPoolExecutor

def calculateCost(distance: float):
  if distance == 0:
    return 0
  if distance <= 1:
    return 35
  if distance <= 10: # 0 - 10
    return 35 + distance * 5.5
  if distance <= 20: # 10 - 20
    return 35 + 55 + ((distance - 10) * 6.5)
  if distance <= 40: # 20 - 40
    return 35 + 55 + 65 + ((distance - 20) * 7.5)
  if distance <= 60: # 40 - 60
    return 35 + 55 + 65 + 75 + ((distance - 40) * 8)
  if distance <= 80: # 60 - 80
    return 35 + 55 + 65 + 75 + 80 + ((distance - 60) * 9)
  return 35 + 55 + 65 + 75 + 80 + 90 + ((distance - 80) * 10.5)

class Node(NamedTuple):
  origins: str
  destination: str
  distance: int
  duration: int
  cost: int

fixedLocation = {
  "BTS พหลโยธิน 59": "13.882596035785667, 100.60077581521406",
  "BTS กรมทหารราบที่ 11": "13.867823363326066, 100.59209494119311",
  "BTS พหลโยธิน 24": "13.824587157649663, 100.56647456041438",
  "MRT ภาษีเจริญ": "13.713090600669332, 100.43446991657855",
  "BTS ศรีนครินทร์": "13.59251158626886, 100.60882372934867",
  "BTS แยก คปอ.": "13.92403741866221, 100.62523264976284",
  "BTS โรงเรียนนายเรือ": "13.608741800234734, 100.59479705775063",
}

def fetchFromGoogleAPI(origins: str, destinations: str) -> Union[int, int]:
  originsFixed = origins
  destinationsFixed = destinations
  if origins in fixedLocation.keys():
    originsFixed = fixedLocation[origins]
    # print("fixed " + origins + " -> " + originsFixed)
  if destinations in fixedLocation.keys():
    destinationsFixed = fixedLocation[destinations]
    # print("fixed " + destinations + " -> " + destinationsFixed)
  query = {
    "key": "",
    "origins": originsFixed,
    "destinations": destinationsFixed,
  }
  response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", query)
  responseJSON = response.json()
  distance = responseJSON["rows"][0]["elements"][0]["distance"]["value"]
  duration = responseJSON["rows"][0]["elements"][0]["duration"]["value"]
  return distance, duration

def appendNode(origins, destination):
  if origins != destination:
    distance, duration = 0, 0
    try:
      distance, duration = fetchFromGoogleAPI(origins, destination)
      print("Done:  " + origins+" -> "+destination)
    except:
      print("Error: " + origins+" -> "+destination)
    node = Node(origins, destination, distance, duration, calculateCost(distance/1000))
    nodes.append(node)

stationList = json.load(open("station_list.json"))
nodes: list[Node] = []

executor = ThreadPoolExecutor(128)

for origins in stationList:
  for destination in stationList:
    feature = executor.submit(appendNode, origins, destination)
    # appendNode(origins, destination)

feature.result()

jsonNodes: list[str] = []
for node in nodes:
  jsonNodes.append(node._asdict())

with open('taxi-nodes.json', 'w', encoding='utf8') as outfile:
  json.dump(jsonNodes, outfile, indent=2, ensure_ascii=False)
