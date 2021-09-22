import re
from classes import NodeMap

def findInNodeMaps(dataNodes, origins: str, destination: str):
  for dataNode in dataNodes:
    if (dataNode['origins'] == origins and dataNode['destination'] == destination):
      return NodeMap(dataNode['origins'], dataNode['destination'], dataNode['duration'], dataNode['cost'], dataNode['origins']+'->'+dataNode['destination'])
  return None

def findInterChangeNodeMaps(interchangeList: list[str], interchangeDataNode, dataNodes, origins: str):
  interchanges: list[NodeMap] = []
  if (interchangeList.count(origins) > 0):
    interchangeDestination = getInterchangeDestination(interchangeDataNode, origins)
    if interchangeDestination != None:
      interchanges.append(NodeMap(origins, interchangeDestination, 0, 0, origins+'->'+interchangeDestination))
    else:
      raise SyntaxError("interchange destination not found")
  for dataNode in dataNodes:
    if (dataNode['origins'] == origins and interchangeList.count(dataNode['destination']) > 0):
      # print(dataNode)
      interchangeDestination = getInterchangeDestination(interchangeDataNode, dataNode['destination'])
      if interchangeDestination != None:
        interchanges.append(NodeMap(dataNode['origins'], interchangeDestination, dataNode['duration'], dataNode['cost'], dataNode['origins']+'->'+dataNode['destination']+'->'+interchangeDestination))
      else:
        raise SyntaxError("interchange destination not found")
  return interchanges

def getInterchangeOriginList(interchangeDataNode):
  originList: list[str] = []
  for dataNode in interchangeDataNode:
    originList.append(dataNode['origins'])
  return originList

def getInterchangeDestination(interchangeDataNode, origins):
  for dataNode in interchangeDataNode:
    if (dataNode['origins'] == origins):
      return dataNode['destination']
  return None

def getVehicleType(name: str):
  if re.search("^BTS", name) != None:
    return "BTS"
  if re.search("^MRT", name) != None:
    return "MRT"
  return "AIR PORT LINK"
  # name.