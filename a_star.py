from functions import findInNodeMaps, findInterChangeNodeMaps, getInterchangeOriginList, getVehicleType
from classes import Node
import json

inputData = json.load(open('input.json'))

interchangeNodes = json.load(open('data/nodes-inter.json'))
btsNodes = json.load(open('data/nodes-bts.json'))
mrtNodes = json.load(open('data/nodes-mrt.json'))
aprNodes = json.load(open('data/nodes-apr.json'))
taxiNodes = json.load(open('data/nodes-taxi.json'))

interchangeOriginList = getInterchangeOriginList(interchangeNodes)

origins = inputData['origins']
start_node = Node(0, [origins], origins, "-", 0, 0, 0, [origins])
goal = inputData['goal'] # MRT คลองเตย, BTS นานา, BTS คูคต, AIR PORT LINK BAN THAP CHANG
last_index = 0

# 1:1 default multiplier is 12.5
durationWeight = float(inputData['durationWeight'])
costWeight = float(inputData['costWeight'])

def calculateCost(duration: float, cost: float):
  return (duration * durationWeight) + (cost * costWeight * 12.5)

def getNewID():
  global last_index
  last_index = last_index + 1
  return last_index

def gen_successors(node: Node):
  successors: list[Node] = []

  # BTS direct
  btsNodeMap = findInNodeMaps(btsNodes, node.state, goal)
  if btsNodeMap != None:
    if node.visitedStations.count(btsNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [btsNodeMap.destination], btsNodeMap.destination, 'BTS', node.costMoney + btsNodeMap.cost, node.costDuration + btsNodeMap.duration, node.f + calculateCost(btsNodeMap.duration, btsNodeMap.cost), node.route + [btsNodeMap.description]))

  # BTS to interchange
  interchangeNodeMaps = findInterChangeNodeMaps(interchangeOriginList, interchangeNodes, btsNodes, node.state)
  for interchangeNodeMap in interchangeNodeMaps:
    if node.visitedStations.count(interchangeNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [interchangeNodeMap.destination], interchangeNodeMap.destination, getVehicleType(interchangeNodeMap.destination), node.costMoney + interchangeNodeMap.cost, node.costDuration + interchangeNodeMap.duration, node.f + calculateCost(interchangeNodeMap.duration, interchangeNodeMap.cost), node.route + [interchangeNodeMap.description]))

  # MRT direct
  mrtNodeMap = findInNodeMaps(mrtNodes, node.state, goal)
  if mrtNodeMap != None:
    if node.visitedStations.count(mrtNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [mrtNodeMap.destination], mrtNodeMap.destination, 'MRT', node.costMoney + mrtNodeMap.cost, node.costDuration + mrtNodeMap.duration, node.f + calculateCost(mrtNodeMap.duration, mrtNodeMap.cost), node.route + [mrtNodeMap.description]))

  # MRT to interchange
  interchangeNodeMaps = findInterChangeNodeMaps(interchangeOriginList, interchangeNodes, mrtNodes, node.state)
  for interchangeNodeMap in interchangeNodeMaps:
    if node.visitedStations.count(interchangeNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [interchangeNodeMap.destination], interchangeNodeMap.destination, getVehicleType(interchangeNodeMap.destination), node.costMoney + interchangeNodeMap.cost, node.costDuration + interchangeNodeMap.duration, node.f + calculateCost(interchangeNodeMap.duration, interchangeNodeMap.cost), node.route + [interchangeNodeMap.description]))

  # APR direct
  aprNodeMap = findInNodeMaps(aprNodes, node.state, goal)
  if aprNodeMap != None:
    if node.visitedStations.count(aprNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [aprNodeMap.destination], aprNodeMap.destination, 'MRT', node.costMoney + aprNodeMap.cost, node.costDuration + aprNodeMap.duration, node.f + calculateCost(aprNodeMap.duration, aprNodeMap.cost), node.route + [aprNodeMap.description]))

  # APR to interchange
  interchangeNodeMaps = findInterChangeNodeMaps(interchangeOriginList, interchangeNodes, aprNodes, node.state)
  for interchangeNodeMap in interchangeNodeMaps:
    if node.visitedStations.count(interchangeNodeMap.destination) == 0: # visited station check
      successors.append(Node(getNewID(), node.visitedStations + [interchangeNodeMap.destination], interchangeNodeMap.destination, getVehicleType(interchangeNodeMap.destination), node.costMoney + interchangeNodeMap.cost, node.costDuration + interchangeNodeMap.duration, node.f + calculateCost(interchangeNodeMap.duration, interchangeNodeMap.cost), node.route + [interchangeNodeMap.description]))

  # taxi direct
  taxtNodeMap = findInNodeMaps(taxiNodes, node.state, goal)
  if taxtNodeMap != None:
    successors.append(Node(getNewID(), node.visitedStations + [taxtNodeMap.destination], taxtNodeMap.destination, 'Taxi', node.costMoney + taxtNodeMap.cost, node.costDuration + taxtNodeMap.duration, node.f + calculateCost(taxtNodeMap.duration, taxtNodeMap.cost), node.route + [taxtNodeMap.description]))

  # for successor in successors:
  #   print(successor)
  return successors

def is_goal(node: Node):
  return node.state == goal

def sortFringeByF(node: Node):
  return node.f

def insert_all(node: Node, fringe: list[Node]):
  children = gen_successors(node)
  for child in children:
    fringe.append(child)
  fringe.sort(key=sortFringeByF)
  # print('-------FRINGE-------')
  # for f in fringe:
  #   print(f)

def show_result(node: Node):
  print('-------RESULT-------')
  print(node)
    
def a_star(start_node: Node):
  # global last_index
  # global visited_node 
  # global total_expanded_nodes 

  fringe = [start_node]
  while True:
    if len(fringe) == 0:
      print('Not Found')
      break
    front = fringe[0]
    fringe = fringe[1:]
    if is_goal(front):
      show_result(front)
      return
    insert_all(front,fringe)

a_star(start_node) # (state,node_id,parent_id,depth,cost,f)
# gen_successors(start_node)
